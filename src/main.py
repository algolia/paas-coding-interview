import argparse

from argocd.apps import sync_app
from datadog.downtime import get_all_downtimes_200, is_downtime_active, remove_downtime
from utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="pass", description="deploy + datadog", epilog="Help")
    parser.add_argument("sync")  # positional argument
    parser.add_argument("--application_name")  # option that takes a value
    args = parser.parse_args()
    application_name = args.application_name
    logger.info("Starting the CLI for appname %s", application_name)
    is_downtime_active = is_downtime_active(application_name)
    if not is_downtime_active:
        schedule_downtime(application_name)
    is_downtime_active = True
    is_apped_sync, downtime_id = sync_app(application_name)
    if is_apped_sync:
        remove_downtime(downtime_id)
