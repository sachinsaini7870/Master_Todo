from datetime import datetime, timezone


def utcnow() -> datetime:
    """Timezone-aware UTC now."""
    return datetime.now(timezone.utc)


def start_of_utc_day(dt: datetime | None = None) -> datetime:
    dt = dt or utcnow()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
