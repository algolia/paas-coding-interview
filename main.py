# tracking file content
# dattime - current oepration (pr chec, dd downtime created, argo cd sync triggerd )

# timer for the tracking of the downtime
# 200 201 > save to file the progress dd-downtome started
# update downtim started in trakcign file
# call argocd sync + foreground sync + timeout (with a meansure one vs previous deployment)
# update downtim started in trakcign file started sync
# loop 5 retries of 30sectimeout
# if timout hits => we have long img pull or error
# check the actual sync status of the app
# if it failes
# faield after 5 reties and x min of timout, rollback
# notify person either through cli promt or with slack + not healthy components
# if the human in the loop agrees ! ->
# rollback argo level to previous version
# end retry loop
# if it succeed
# notify slakc + print sucess + track in the file
# remove downtime dd api
# update tracking to don at x

import argparse
import json
import logging
import os
import sys
import time
from datetime import UTC, datetime, timedelta

import requests

log = logging.getLogger("probe.cli")

HTTPBIN_URL = os.environ.get("HTTPBIN_URL", "https://httpbin.org")
DOWNTIME_MINUTES = 30
SYNC_RETRIES = 5
SYNC_WAIT = int(os.environ.get("SYNC_WAIT", "30"))


class GitHubError(Exception):
    """GitHub API call failed."""


class DatadogError(Exception):
    """Datadog API call failed."""


class ArgoCDError(Exception):
    """ArgoCD API call failed."""


def call_httpbin(method, path, fake, timeout, error_cls):
    """httpbin /anything echoes `fake` back: fake data, real network and errors."""
    url = f"{HTTPBIN_URL}/anything/{path}"
    try:
        resp = requests.request(method, url, json=fake, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise error_cls(f"{method} {path}: {e}") from e
    return resp.json()["json"]


def call_gh_api(pr_num):
    # GET /repos/{owner}/{repo}/pulls/{pr_num}
    fake = {"number": pr_num, "merged": True, "checks": "success"}
    return call_httpbin("GET", f"pulls/{pr_num}", fake, 10, GitHubError)


def read_progress_file(file_pt):
    try:
        with open(file_pt) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def update_progress_file(file_pt, progress, **fields):
    state = read_progress_file(file_pt)
    now = datetime.now(UTC).isoformat(timespec="seconds")
    state.update(fields, step=progress)
    state.setdefault("history", []).append(f"{now} {progress}")
    with open(f"{file_pt}.tmp", "w") as f:
        json.dump(state, f, indent=2)
    os.replace(f"{file_pt}.tmp", file_pt)  # atomic: no half-written file on crash
    log.info("tracking: %s", progress)
    return state


def call_dd_api(action, app_name=None, dt_id=None, minutes=DOWNTIME_MINUTES):
    # call dd api
    end = datetime.now(UTC) + timedelta(minutes=minutes)
    schedule = {"end": end.isoformat(timespec="seconds")}
    if action == "create_downtime":
        # POST /api/v2/downtime; the end makes the mute expire if this CLI dies
        scope = {"monitor_tags": [f"app:{app_name}"]}
        fake = {
            "data": {
                "id": "dt-123",
                "attributes": {"monitor_identifier": scope, "schedule": schedule},
            }
        }
        return call_httpbin("POST", "api/v2/downtime", fake, 10, DatadogError)["data"][
            "id"
        ]
    if action == "update_downtime":
        # PATCH /api/v2/downtime/{dt_id}
        fake = {"data": {"id": dt_id, "attributes": {"schedule": schedule}}}
        return call_httpbin("PATCH", f"api/v2/downtime/{dt_id}", fake, 10, DatadogError)
    if action == "cancel_downtime":
        # DELETE /api/v2/downtime/{dt_id}
        return call_httpbin("DELETE", f"api/v2/downtime/{dt_id}", {}, 10, DatadogError)
    raise DatadogError(f"unknown action: {action}")


def call_argocd_api(app_name, action, timeout):
    # call dd api
    path = f"api/v1/applications/{app_name}"
    if action == "sync":
        # POST /api/v1/applications/{name}/sync
        return call_httpbin(
            "POST", f"{path}/sync", {"revision": "HEAD"}, timeout, ArgoCDError
        )
    if action == "sync_status":
        # GET /api/v1/applications/{name} -> status.sync.status, status.health.status
        health = os.environ.get("FAKE_HEALTH", "Healthy")
        fake = {"sync": "Synced", "health": health}
        return call_httpbin("GET", path, fake, timeout, ArgoCDError)
    if action == "rollback":
        # POST /api/v1/applications/{name}/rollback with the previous history id
        return call_httpbin(
            "POST", f"{path}/rollback", {"id": 41}, timeout, ArgoCDError
        )
    raise ArgoCDError(f"unknown action: {action}")


def wait_for_sync(app_name):
    for attempt in range(1, SYNC_RETRIES + 1):
        status = call_argocd_api(app_name, "sync_status", timeout=SYNC_WAIT)
        log.info(
            "attempt %d/%d: sync=%s health=%s",
            attempt,
            SYNC_RETRIES,
            status["sync"],
            status["health"],
        )
        if status["sync"] == "Synced" and status["health"] == "Healthy":
            return
        if attempt < SYNC_RETRIES:
            time.sleep(SYNC_WAIT)
    raise ArgoCDError(
        f"not healthy after {SYNC_RETRIES} x {SYNC_WAIT}s (long img pull or error)"
    )


def notify_user(message):
    log.warning("notify (slack stub): %s", message)


def ask_rollback(app_name):
    if not sys.stdin.isatty():
        log.warning("no terminal, no human to ask: skipping rollback")
        return False
    return (
        input(f"rollback {app_name} to previous version? [y/N] ").strip().lower() == "y"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check HTTP endpoints.")
    sync_sub = parser.add_subparsers(
        dest="command",
        required=True,
        title="sync",
        description="sync application to ArgoCD",
    )
    sync_parser = sync_sub.add_parser("sync")
    # j
    sync_parser.add_argument("application_name")
    sync_parser.add_argument("--pr-number", type=int, default=4)
    sync_parser.add_argument("-v", "--verbose", action="store_true")

    log.info("extract args")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    app_name = args.application_name
    pr_num = args.pr_number
    file_pt = f"tracking-{app_name}-{pr_num}.json"

    state = read_progress_file(file_pt)
    if state.get("step") == "done":
        log.info("already done for %s pr %s, nothing to do", app_name, pr_num)
        return 0
    log.info("started sync for %s for pr %s tracking file", app_name, pr_num)
    update_progress_file(file_pt, "Started", app=app_name, pr=pr_num)

    log.info("check pr status + check merge status")
    try:
        pr_status = call_gh_api(pr_num)
    except GitHubError as e:
        log.error("pr check failed: %s", e)
        return 1
    if not (pr_status["merged"] and pr_status["checks"] == "success"):
        log.error("pr %s not merged or checks not green, abording", pr_num)
        update_progress_file(file_pt, "aborted: pr not ready")
        return 1

    log.info("call dd api for trigger dwontime for app_nam")
    dt_id = state.get("dt_id")  # resume: reuse the downtime of a crashed run
    if not dt_id:
        try:
            dt_id = call_dd_api("create_downtime", app_name=app_name)
        except DatadogError as e:
            log.error("dd downtime failed abording: %s", e)
            update_progress_file(file_pt, "aborted: downtime failed")
            return 1
        update_progress_file(file_pt, "downtime started", dt_id=dt_id)

    try:
        call_argocd_api(app_name, "sync", timeout=60 * 10)
        update_progress_file(file_pt, "started sync")
        wait_for_sync(app_name)
    except ArgoCDError as e:
        log.error("sync failed: %s", e)
        update_progress_file(file_pt, "sync failed")
        notify_user(f"{app_name} sync failed: {e}")
        if ask_rollback(app_name):
            call_dd_api("update_downtime", dt_id=dt_id, minutes=15)
            call_argocd_api(app_name, "rollback", timeout=60 * 10)
            update_progress_file(file_pt, "rolled back")
        return 1
    finally:
        # always unmute: on failure the alerts are real
        try:
            call_dd_api("cancel_downtime", dt_id=dt_id)
            update_progress_file(file_pt, "downtime removed", dt_id=None)
        except DatadogError:
            log.exception("could not remove downtime %s, remove it by hand", dt_id)

    notify_user(f"{app_name} synced (pr {pr_num})")
    update_progress_file(file_pt, "done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
