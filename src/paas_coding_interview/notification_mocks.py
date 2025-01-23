def send_slack_message(channel: str, message: str) -> bool:
    """
    Mock sending a Slack message to a channel
    Returns True if message was sent successfully, False otherwise
    
    For testing: Messages to 'invalid-channel' will fail
    """
    if channel == "invalid-channel":
        return False
    return True

