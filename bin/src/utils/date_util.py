from datetime import UTC, datetime


def from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp / 1000, tz=UTC)

def get_now() -> datetime:
    return datetime.now(UTC)

def to_string(datetime: datetime, format: str = "%Y-%m-%dT%H:%M:%S.%fZ") -> str:
    return datetime.strftime(format)
