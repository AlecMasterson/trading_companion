from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def get_time_et(offset_days: int = 0) -> datetime:
    return datetime.now(ZoneInfo("America/New_York")) + timedelta(days=offset_days)


def to_iso_8601(timestamp: int) -> str:
    date: datetime = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    return date.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def to_string(date: datetime, format: str = "%Y-%m-%d") -> str:
    return date.strftime(format)
