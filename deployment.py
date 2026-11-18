from datadog_api_client.v2.model.downtime_create_request import DowntimeCreateRequest
from datadog_api_client.v2.model.downtime_resource_type import DowntimeResourceType
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.downtimes_api import DowntimesApi

import time
import requests
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

max_tries = 5


# Create a maintenance window in datadog

def create_maintenance_window(application_name: str) -> str:
    body = DowntimeCreateRequest(
    data=DowntimeCreateRequestData(
        attributes=DowntimeCreateRequestAttributes(
            message="Maintenance window",
            scope="test:{application_name}",
        ),
        type=DowntimeResourceType.DOWNTIME,
        ),
    )


    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = DowntimesApi(api_client)
        response = api_instance.create_downtime(body=body)

        return response.json()["data"][0]["id"]  # 00000000-0000-1234-0000-000000000000
    

# todo ;: implement maintenance window check




def deploy_to_argocd(application_name: str) -> bool:
    api_url = "https://cd.apps.argoproj.io/api/v1/applications/{application_name}/sync"
    response = requests.post(api_url)
    if response.status == 200:
        return True
    return False


def remove_maintenance_window(downtime_id: str)  -> bool:
    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = DowntimesApi(api_client)
        api_instance.cancel_downtime(
            downtime_id=downtime_id,
        )
        return True


def main():
    current_try = 0
    application_name = sys.argv[1]
    maintenance_window_id = create_maintenance_window(application_name)
    if maintenance_window_id:
        while current_try < max_tries:
            result = deploy_to_argocd(application_name)
            if result:
                break
            else:
                current_try+=1
                time.sleep(current_try ** 2)

    
    remove_maintenance_window(maintenance_window_id)
    

