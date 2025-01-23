import os
from functools import wraps
from typing import Type, Callable
from paas_coding_interview.notification_mocks import send_slack_message

def notify_error_in_ci(error_channel: str = "#deployments-errors") -> Callable:
    """
    Decorator factory that sends notifications to Slack when in CI environment
    before re-raising the original error
    """
    def decorator(error_class: Type[Exception]) -> Type[Exception]:
        if not os.getenv("CI"):
            return error_class
            
        class NotifiedError(error_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                send_slack_message(
                    channel=error_channel,
                    message=f"Error in CI: {str(self)}"
                )
        
        NotifiedError.__name__ = error_class.__name__
        return NotifiedError
    
    return decorator

# Example usage:
@notify_error_in_ci()
class ApplicationNotFoundError(Exception):
    """Raised when application is not found in registry"""
    def __init__(self, application_name: str = None):
        message = f"Application '{application_name}' not found in registry" if application_name else "Application not found in registry"
        super().__init__(message)

@notify_error_in_ci()
class ApplicationIsDownError(Exception):
    """Raised when trying to deploy an application that is down"""
    def __init__(self, application):
        message = f"Application '{application.name}' is currently down. Could not deploy."
        if application.downtime and application.downtime.downtime_id:
            message += f" (downtime_id: {application.downtime.downtime_id})"
        super().__init__(message)

@notify_error_in_ci()
class ApplicationSyncError(Exception):
    """Raised when trying to sync an application that failed"""
    def __init__(self, application):
        message = f"Application '{application.name}' failed to sync to Argo CD. Could not deploy."
        super().__init__(message)