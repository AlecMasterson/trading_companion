from datetime import UTC, datetime
from zoneinfo import ZoneInfo

def from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp / 1000, tz=UTC)

def get_now() -> datetime:
    return datetime.now(UTC)

def get_now_eastern() -> datetime:
    return datetime.now(UTC).astimezone(ZoneInfo("America/New_York"))

def to_string(datetime: datetime, format: str = "%Y-%m-%dT%H:%M:%S.%fZ") -> str:
    return datetime.strftime(format)
