from datetime import datetime, timedelta
import pytz


# ---------------------------------------------
# CONSTANT TIMEZONES
# ---------------------------------------------
UTC = pytz.utc
IST = pytz.timezone("Asia/Kolkata")


# ---------------------------------------------
# 1. GET CURRENT UTC TIME (BEST PRACTICE)
# ---------------------------------------------
def now_utc():
    """
    Returns current UTC datetime (naive UTC or aware UTC).
    Always prefer storing UTC in database.
    """
    return datetime.utcnow()


# ---------------------------------------------
# 2. CONVERT UTC → IST
# ---------------------------------------------
def utc_to_ist(dt):
    """
    Converts a UTC datetime to Indian Standard Time (IST).
    Works for both naive and timezone-aware UTC datetimes.
    """
    if dt is None:
        return None

    # If datetime is naive, assume it's UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    return dt.astimezone(IST)


# ---------------------------------------------
# 3. CONVERT IST → UTC
# ---------------------------------------------
def ist_to_utc(dt):
    """
    Converts an IST datetime to UTC. Useful for parsing user-submitted times.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        dt = IST.localize(dt)

    return dt.astimezone(UTC)


# ---------------------------------------------
# 4. FORMAT DATETIME AS ISO 8601 STRING
# ---------------------------------------------
def to_iso(dt):
    """
    Returns datetime in ISO8601 format.
    Example: '2025-02-03T10:20:30+05:30'
    """
    if dt is None:
        return None

    # Assume it's UTC if naive
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    return dt.isoformat()


# ---------------------------------------------
# 5. PARSE ISO STRING → DATETIME
# ---------------------------------------------
def parse_iso(dt_str):
    """
    Converts ISO8601 string to datetime object.
    """
    if not dt_str:
        return None

    return datetime.fromisoformat(dt_str)


# ---------------------------------------------
# 6. CHECK IF DATETIME HAS EXPIRED (Useful for OTP, forgot-password)
# ---------------------------------------------
def is_expired(expiry_dt):
    """
    Returns True if current UTC time is greater than expiry time.
    """
    if expiry_dt is None:
        return True

    now = now_utc()

    # Convert expiry to UTC if naive
    if expiry_dt.tzinfo is None:
        expiry_dt = expiry_dt.replace(tzinfo=UTC)

    return now.replace(tzinfo=UTC) > expiry_dt


# ---------------------------------------------
# 7. CREATE EXPIRATION TIME (e.g. OTP, tokens)
# ---------------------------------------------
def expires_in(minutes=5):
    """
    Returns a future datetime in UTC.
    Useful for OTP or password reset tokens.
    """
    return now_utc() + timedelta(minutes=minutes)


# ---------------------------------------------
# 8. HUMAN READABLE DATE FORMAT (Optional)
# ---------------------------------------------
def human_readable(dt):
    """
    Example output:
    '03 Feb 2025, 10:30 AM'
    """
    if dt is None:
        return None

    dt = utc_to_ist(dt)
    return dt.strftime("%d %b %Y, %I:%M %p")
