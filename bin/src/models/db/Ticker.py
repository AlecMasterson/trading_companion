from sqlmodel import Field, SQLModel

class Ticker(SQLModel, table=True):

    __table_args__ = {
        "schema": "market_data"
    }
    __tablename__ = "tickers"

    name: str
    ticker: str = Field(primary_key=True)
