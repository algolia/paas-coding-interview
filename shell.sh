#!/bin/bash

set +euo pipefail
file_name=$1
app_name=$1

if [ -z "$file_name" ]; then
  echo "Usage: $0 <file_name> [app_name]"
  exit 1
fi

if [ -z "$app_name" ]; then
  app_name=$(basename "$file_name")
fi

# run the script with in verbose mode use "./script.sh app_name -v"
set -x
# to run the script with in debug mode

app_name=0
activate_datadog_downtime=0
trigger_argocd=0
deactivate_datadog_downtime=0
downtime_id=null

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $"
}

activate_datadog() {
  echo "Activating Datadog downtime for $app_name..."
  # Add your Datadog API call here to activate downtime
  update activate_datadog_downtime=1
  catch(activate_datadog_downtime) {
    echo "Error activating Datadog downtime for $app_name"
    exit 1
  }

  log()
  adding_timeout(
  )
 
  curl -X POST "https://api.datadoghq.com/api/v2/downtime" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-d @- << EOF
{
  "data": {
    "attributes": {
      "display_timezone": "America/New_York",
      "message": "Message about the downtime",
      "monitor_identifier": {
        "monitor_id": 123
      },
      "mute_first_recovery_notification": false,
      "notify_end_states": [
        "alert",
        "warn"
      ],
      "notify_end_types": [
        "canceled",
        "expired"
      ],
      "schedule": {
        "timezone": "America/New_York"
      },
      "scope": "env:(staging OR prod) AND datacenter:us-east-1"
    },
    "type": "downtime"
  }
}
EOF
 downtime_id="app_name.random_value" # Replace with actual downtime ID from Datadog response

}

trigger_argocd_sync() {
  echo "Triggering ArgoCD sync for $app_name..."
  # Add your ArgoCD API call here to trigger sync
  app_name=
  argo_cd=
  relevent
  trigger_argocd=1

    log()

}

deactivate_datadog() {
  echo "Deactivating Datadog downtime for $app_name..."
  # Add your Datadog API call here to deactivate downtime
  datadog_api_key=
  deactivate_datadog=1
  log()
}

case ("$1") in
  activate)
    activate_datadog 
    ;;
  trigger)
    trigger_argocd_sync
    ;;
  deactivate)
    deactivate_datadog
    ;;
  *)
    echo "Usage: $0 {activate|trigger|deactivate}"
    exit 1
    ;;
esac

main() {
while true; do
  activate_datadog=1    
  trigger_argocd_sync=1
  deactivate_datadog=1

}

# once the script is executed, then cleanup the 


