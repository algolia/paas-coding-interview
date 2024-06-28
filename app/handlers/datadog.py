import logging

import requests


class DatadogHandler:
    def __init__(self, application_name: str):
        self.application_name = application_name
        self.logger = logging.getLogger(self.__class__.__name__)
        self.base_url = "https://api.datadoghq.com/api/v2"
        self.headers = {}

    def activate_datadog_downtime(self):
        url = f"{self.base_url}/downtime"

        # Implementation of a easy mock
        # response = requests.post(
        #     url,
        #     self.headers,
        # )

        # response.json()["data"]["id"]

        return {"message": "Activate Datadog Downtime OK"}

    def remove_datadog_downtime(self):
        return {"message": "Remove Datadog Downtime OK"}
