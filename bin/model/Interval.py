import enum


class Interval(enum.Enum):

    MINUTE_1 = "MINUTE_1"
    MINUTE_5 = "MINUTE_5"
    MINUTE_15 = "MINUTE_15"
    HOUR_1 = "HOUR_1"
    HOUR_6 = "HOUR_6"
    DAY_1 = "DAY_1"

    def __str__(self):
        return self.value

    def get_seconds(self) -> int:
        return {
            Interval.MINUTE_1: 60,
            Interval.MINUTE_5: 60 * 5,
            Interval.MINUTE_15: 60 * 15,
            Interval.HOUR_1: 60 * 60,
            Interval.HOUR_6: 60 * 60 * 6,
            Interval.DAY_1: 60 * 60 * 24,
        }[self]
