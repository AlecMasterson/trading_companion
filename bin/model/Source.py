import enum


class Source(enum.Enum):

    BINANCE = "BINANCE"
    COINBASE = "COINBASE"

    def __str__(self):
        return self.value
