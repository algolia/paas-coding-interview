# Mock data to simulate Datadog API responses
# We assume that Datadog API can give us downtime IDs from a specific application name

from paas_coding_interview.models import Downtime

# Simulate a set of active downtimes that would be DD source of truth
_active_downtimes = set()


def get_downtime(application_name: str) -> Downtime:
    """
    Mock checking if an application has an active downtime
    Returns a Downtime object with active status and optional ID
    """
    # Simulate an application that's already in downtime
    if application_name == "app-in-downtime":
        return Downtime(active=True, downtime_id="mock-downtime-123")
    
    # Default case - no active downtime
    return Downtime(active=False)

def has_downtime(application_name: str) -> bool:
    """
    Check if application has an active downtime
    Returns True if downtime exists, False otherwise
    """
    return get_downtime(application_name).active

def schedule_downtime(application_name: str) -> Downtime:
    """
    Schedule a downtime for an application
    Returns a Downtime object with the new downtime details
    """
    _active_downtimes.add(application_name)
    return Downtime(active=True, downtime_id="mock-downtime-456")

def unset_downtime(downtime_id: str) -> Downtime:
    """
    Remove a downtime using its ID
    Returns a Downtime object with the updated status
    """
    return Downtime(active=False)