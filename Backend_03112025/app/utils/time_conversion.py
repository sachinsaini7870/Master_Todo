# from datetime import datetime
import pytz

def to_indianStandardTime(dt):
    if dt is None:
        return None

    # If dt is naive (no timezone)
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    ist = pytz.timezone("Asia/Kolkata")
    return dt.astimezone(ist)

