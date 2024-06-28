import logging


class ArgoCDHandler:
    def __init__(self, application_name: str):
        self.application_name = application_name
        self.logger = logging.getLogger(self.__class__.__name__)

    def trigger_argocd_sync(self):
        return {"message": "Trigger ArgoCD OK"}
