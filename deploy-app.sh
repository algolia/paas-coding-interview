#!/usr/bin/env bash
#
# Deployment sync CLI (shell implementation)
# Workflow: Datadog downtime on → Argo CD sync → Datadog downtime off
# Idempotent: progress is stored under state/ and resumed on re-run after failure.
#
# Usage: ./sync.sh <application_name>
#        ./sync.sh -v my-app

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="${SCRIPT_DIR}/state"
VERBOSE=0

log_info()  { echo "INFO  $*" >&2; }
log_error() { echo "ERROR $*" >&2; }
log_debug() { [[ "${VERBOSE}" -eq 1 ]] && echo "DEBUG $*" >&2 || true; }

usage() {
  cat <<'EOF'
Usage: sync.sh [-v] <application_name>

Run deployment workflow:
  1. Activate Datadog downtime (mock)
  2. Trigger Argo CD application sync (mock)
  3. Remove Datadog downtime (mock)

Options:
  -v    Verbose logging to stderr

On failure, state is kept in state/<application_name>.env — re-run the same command to resume.
EOF
}

# --- State (idempotency) -------------------------------------------------------

state_file() {
  mkdir -p "${STATE_DIR}"
  echo "${STATE_DIR}/${1}.env"
}

state_init_file() {
  local file="$1"
  cat >"${file}" <<'EOF'
datadog_downtime_activated=0
argocd_trigger_synced=0
datadog_downtime_removed=0
datadog_downtime_id=
EOF
}

state_load() {
  local app="$1"
  local file
  file="$(state_file "${app}")"
  if [[ ! -f "${file}" ]]; then
    state_init_file "${file}"
  fi
  # shellcheck source=/dev/null
  source "${file}"
}

state_read_key() {
  local app="$1" key="$2"
  grep "^${key}=" "$(state_file "${app}")" | cut -d= -f2- || true
}

state_set() {
  local app="$1" key="$2" value="$3"
  local file
  file="$(state_file "${app}")"
  if [[ ! -f "${file}" ]]; then
    state_init_file "${file}"
  fi
  if grep -q "^${key}=" "${file}"; then
    sed -i "s|^${key}=.*|${key}=${value}|" "${file}"
  else
    echo "${key}=${value}" >>"${file}"
  fi
  # Keep in-memory copy in sync when running in same process
  printf -v "${key}" '%s' "${value}"
}

state_is_step_completed() {
  local app="$1" step="$2"
  [[ "$(state_read_key "${app}" "${step}")" == "1" ]]
}

state_mark_step_completed() {
  local app="$1" step="$2"
  state_set "${app}" "${step}" "1"
  log_debug "Marked step completed: ${step}"
}

state_clear() {
  local app="$1"
  local file
  file="$(state_file "${app}")"
  [[ -f "${file}" ]] && rm -f "${file}"
  log_debug "Cleared state for ${app}"
}

# --- Mock: Datadog (https://docs.datadoghq.com/api/latest/downtimes/) ----------

mock_datadog_downtime_id() {
  echo "mock-downtime-${1}"
}

mock_activate_datadog_downtime() {
  local app="$1" downtime_id="${2:-}"
  if [[ -z "${downtime_id}" ]]; then
    downtime_id="$(mock_datadog_downtime_id "${app}")"
  fi
  log_info "Datadog downtime active id=${downtime_id}"
  cat <<EOF
{"data":{"id":"${downtime_id}","type":"downtime","attributes":{"message":"Deployment maintenance for ${app}","scope":["service:${app}"],"active":true,"monitor_identifier":{"monitor_tags":["service:${app}"]}}}}
EOF
}

mock_remove_datadog_downtime() {
  local downtime_id="$1"
  log_info "Datadog downtime removed id=${downtime_id}"
  cat <<EOF
{"data":{"id":"${downtime_id}","type":"downtime","attributes":{"active":false}}}
EOF
}

# --- Mock: Argo CD (https://cd.apps.argoproj.io/swagger-ui) --------------------

mock_trigger_argocd_sync() {
  local app="$1"
  log_info "ArgoCD sync triggered for ${app}"
  cat <<EOF
{"metadata":{"name":"${app}","namespace":"argocd"},"status":{"sync":{"status":"Synced","revision":"abc123def456"},"health":{"status":"Healthy"},"operationState":{"phase":"Succeeded","message":"successfully synced (all tasks ran)"}}}
EOF
}

# --- Workflow ------------------------------------------------------------------

run_workflow() {
  local app="$1"
  state_load "${app}"

  if ! state_is_step_completed "${app}" "datadog_downtime_activated"; then
    local result downtime_id existing_id
    existing_id="$(state_read_key "${app}" "datadog_downtime_id")"
    downtime_id="${existing_id:-$(mock_datadog_downtime_id "${app}")}"
    result="$(mock_activate_datadog_downtime "${app}" "${downtime_id}")"
    echo "${result}"
    state_set "${app}" "datadog_downtime_id" "${downtime_id}"
    state_mark_step_completed "${app}" "datadog_downtime_activated"
    state_load "${app}"
  else
    log_debug "Skipping datadog_downtime_activated (already done)"
  fi

  if ! state_is_step_completed "${app}" "argocd_trigger_synced"; then
    mock_trigger_argocd_sync "${app}"
    state_mark_step_completed "${app}" "argocd_trigger_synced"
    state_load "${app}"
  else
    log_debug "Skipping argocd_trigger_synced (already done)"
  fi

  if ! state_is_step_completed "${app}" "datadog_downtime_removed"; then
    if [[ -z "${datadog_downtime_id:-}" ]]; then
      log_error "Missing datadog_downtime_id; cannot remove downtime."
      return 1
    fi
    mock_remove_datadog_downtime "${datadog_downtime_id}"
    state_mark_step_completed "${app}" "datadog_downtime_removed"
  else
    log_debug "Skipping datadog_downtime_removed (already done)"
  fi

  return 0
}

sync_cmd() {
  local app="$1"
  local state_path
  state_path="$(state_file "${app}")"

  if ! run_workflow "${app}"; then
    log_error "Deployment failed for ${app}. State saved at ${state_path} — re-run the same command to resume."
    exit 1
  fi

  state_clear "${app}"
  log_info "Deployment workflow completed for ${app}"
}

# --- CLI -----------------------------------------------------------------------

main() {
  local application_name=""

  while getopts ":hv" opt; do
    case "${opt}" in
      v) VERBOSE=1 ;;
      h) usage; exit 0 ;;
      *) usage; exit 2 ;;
    esac
  done
  shift $((OPTIND - 1))

  if [[ $# -ne 1 ]]; then
    usage
    exit 2
  fi
  application_name="$1"

  if [[ ! "${application_name}" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]]; then
    log_error "Invalid application_name: ${application_name}"
    exit 2
  fi

  sync_cmd "${application_name}"
}

main "$@"
