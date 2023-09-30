from enum import Enum


class Granularity(Enum):

    MINUTE_1 = "MINUTE_1"
    MINUTE_5 = "MINUTE_5"
    MINUTE_15 = "MINUTE_15"
    HOUR_1 = "HOUR_1"
    HOUR_6 = "HOUR_6"
    DAY_1 = "DAY_1"

    def get_seconds(self) -> int:
        return {
            Granularity.MINUTE_1: 60,
            Granularity.MINUTE_5: 60 * 5,
            Granularity.MINUTE_15: 60 * 15,
            Granularity.HOUR_1: 3600,
            Granularity.HOUR_6: 3600 * 6,
            Granularity.DAY_1: 3600 * 24
        }[self]
