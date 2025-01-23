from dataclasses import dataclass
import json
from typing import List
from paas_coding_interview.models import Application
from paas_coding_interview.datadog_mocks import get_downtime

class ApplicationNotFoundError(Exception):
    """Raised when application is not found in registry"""
    pass

class ApplicationRegistry:
    def __init__(self, applications: List[Application]):
        self.applications = applications

    @classmethod
    def from_argo(cls, repo_path: str):
        # Mock response from /api/v1/applications
        mock_argo_response = {
            "items": [
                {
                    "metadata": {
                        "name": "backend",
                        "namespace": "production",
                    },
                    "spec": {
                        "project": "main"
                    },
                    "status": {
                        "sync": {"status": "Synced"},
                        "health": {"status": "Healthy"}
                    }
                },
                {
                    "metadata": {
                        "name": "failing-app",
                        "namespace": "production",
                    },
                    "spec": {
                        "project": "main"
                    },
                    "status": {
                        "sync": {"status": "OutOfSync"},
                        "health": {"status": "Degraded"}
                    }
                }
            ]
        }

        applications = []
        for app_data in mock_argo_response["items"]:
            app = Application(
                name=app_data["metadata"]["name"],
                namespace=app_data["metadata"]["namespace"],
                project=app_data["spec"]["project"],
                sync_status=app_data["status"]["sync"]["status"],
                health_status=app_data["status"]["health"]["status"],
                downtime=get_downtime(app_data["metadata"]["name"])
            )
            applications.append(app)

        return cls(applications)

    def get_application(self, application_name: str) -> Application:
        for app in self.applications:
            if app.name == application_name:
                return app
        raise ApplicationNotFoundError(f"Application '{application_name}' not found in registry")

# Create a singleton instance of the registry
registry = ApplicationRegistry.from_argo("mock/path")
