# Monscript/CLI sync --appname=monAppli

# Create a downtime on datadof
    #try: API datadog https://docs.datadoghq.com/api/latest/downtimes/schedule-a-downtime/
     # - start / end time
     # monitor-id
#   exept:
   #  logging.error

# try sync on argocd API
    # appname + address
# except: error

# if argocd sync status ok
    # remove datadog downtime

# return exit status

# I would have been better to split all those functions in separate files, difnined by application called (/datadog and /argocd)
# In the end add some unit tests with assert for example to be able to test each function (and the status code returned)

# For argocd we need to check the status of the sync that has been created
# Addind a timeout would be nice to stop listening the status and roll back the changes, REMOVING THE DOWNTIME FROM DATADOG HAS TO BE PERFORMED BEFORE KILLING THE SCRIPT.

import requests, logging, sys

def delete_downtime(downtime_id):
    datadog_url = "http://myurl.com/datadog/" + downtime_id
    response = requests.delete(datadog_url)
    return response.status_code

def create_downtime(monitor_name):
    datadog_url = "http://myurl.com/datadog"
    data = {
    "data": {
        "attributes": {
        "message": "dark forest",
        "monitor_identifier": {
            "monitor_tags": [
            "cat:hat"
            ]
        },
        "scope": "test:exampledowntime",
        "schedule": {
            "start": null
        }
        },
        "type": "downtime"
        }
    }
    response = requests.post(datadog_url, data=data)
    return response.status_code


def create_application_sync(application_name):
    argocd_url = "http://myurl.com/argocd"
    "data"= {
        "appNamespace": "string",
        "dryRun": true,
        "infos": [
            {
            "name": "string",
            "value": "string"
            }
        ],
        "manifests": [
            "string"
        ],
        "name": "string",
        "project": "string",
        "prune": true,
        "resources": [
            {
            "group": "string",
            "kind": "string",
            "name": application_name,
            "namespace": "string"
            }
        ],
        "retryStrategy": {
            "backoff": {
            "duration": "string",
            "factor": 0,
            "maxDuration": "string"
            },
            "limit": 0,
            "refresh": true
        },
        "revision": "string",
        "revisions": [
            "string"
        ],
        "sourcePositions": [
            "string"
        ],
        "strategy": {
            "apply": {
            "force": true
            },
            "hook": {
            "syncStrategyApply": {
                "force": true
            }
            }
        },
        "syncOptions": {
            "items": [
            "string"
            ]
        }
        }
    response = requests.post(argocd_url, data=data)
    return response.status_code



print("enter the application name")
application_name = input()

try: 
    create_downtime("my_application")
    logging.info("Downtime was created")
except ValueError:
    logging.error("Could not create a Downtime on Datadog, %s", ValueError)
    sys.exit(1)

