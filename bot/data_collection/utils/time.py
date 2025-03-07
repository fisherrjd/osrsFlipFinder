import time
from datetime import datetime


def humanize_time(timestamp: int) -> str:
    """Convert Unix timestamp to human-readable format with hours, minutes, and seconds."""

    # Calculate the time difference
    time_diff = time.time() - timestamp

    # Get the number of hours, minutes, and seconds
    hours = int(time_diff // 3600)
    minutes = int((time_diff % 3600) // 60)
    seconds = int(time_diff % 60)

    # Build the human-readable string
    if hours > 0:
        # Show only hours for 1+ hour durations, with singular/plural handling
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif minutes > 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return f"{seconds} second{'s' if seconds > 1 else ''} ago"


def calc_time_range(time_in_minutes):
    current_time = int(datetime.now().timestamp())
    result = current_time - (time_in_minutes * 60)
    return result
