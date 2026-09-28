import requests


def sync_app(application_name: str):
    URL = f"https://cd.apps.argoproj.io/api/v1/applications/{application_name}/sync"

    return True
