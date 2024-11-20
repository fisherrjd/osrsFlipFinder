import time
from datetime import datetime


def humanize_time(timestamp: int) -> str:
    """convert unix -> standard time format"""

    return datetime.utcfromtimestamp(time.time() - timestamp).strftime(
        "%M minutes and %S seconds ago"
    )
