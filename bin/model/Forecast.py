from model.Interval import Interval
from model.Source import Source
import datetime


class Forecast:

    __expected_attributes = [
        ("source", Source),
        ("ticker", str),
        ("interval", Interval),
        ("timestamp", datetime),
        ("price", float),
    ]

    def __init__(self, values: dict) -> None:
        for key in self.__expected_attributes:
            if key[0] in values and isinstance(values[key[0]], key[1]):
                setattr(self, key[0], values[key[0]])
            else:
                setattr(self, key[0], None)
