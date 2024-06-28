import logging

from app.handlers.argo import ArgoCDHandler
from app.handlers.datadog import DatadogHandler
from app.handlers.state import StateHandler


class DeploymentManager:
    def __init__(self, application_name: str):
        self.application_name = application_name
        self.argo = ArgoCDHandler(application_name=application_name)
        self.datadog = DatadogHandler(application_name=application_name)
        self.state = StateHandler(application_name=application_name)
        self.logger = logging.getLogger(self.__class__.__name__)

    def sync(self):
        # Exception handling and state management
        # Step 2: Activate Datadog downtime
        try:
            if not self.state.is_step_completed("datadog_downtime_activated"):
                print(self.datadog.activate_datadog_downtime())
                self.state.mark_step_completed("datadog_downtime_activated")

            # Step 3: Trigger ArgoCD sync
            if not self.state.is_step_completed("argocd_trigger_synced"):
                print(self.argo.trigger_argocd_sync())
                self.state.mark_step_completed("argocd_trigger_synced")
                raise KeyError

            # Step 4: Remove Datadog downtime
            if not self.state.is_step_completed("datadog_downtime_removed"):
                print(self.datadog.remove_datadog_downtime())
                self.state.mark_step_completed("datadog_downtime_removed")
        except Exception as e:  # To improve handling
            pass
        finally:
            self.state.reset_state()
