

def sync(application_name: str) -> tuple[bool, str]:
    """
    Mock Argo CD sync operation
    Returns ArgoSyncStatus with success/failure and message
    """
    if application_name == "failing-app":
        return False, "Failed to sync application, but that's not a real thing, it's just a mock"
    
    return True, "Successfully synced application, but that's not a real thing, it's just a mock"
