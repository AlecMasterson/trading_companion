from dagster import RepositoryDefinition, ScheduleDefinition, job, op, repository
from src.update_ticker_candle_history import main as update_ticker_candle_history
from src.update_tickers import main as update_tickers

@op
def update_ticker_candle_history_op() -> None:
    update_ticker_candle_history()

@job
def update_ticker_candle_history_job() -> None:
    update_ticker_candle_history_op()

@op
def update_tickers_op() -> None:
    update_tickers()

@job
def update_tickers_job() -> None:
    update_tickers_op()

@repository
def main_repository() -> RepositoryDefinition:
    return [
        update_ticker_candle_history_job,
        update_tickers_job,
        ScheduleDefinition(
            job=update_ticker_candle_history_job,
            cron_schedule="0 1 * * *",
            execution_timezone="America/New_York"
        ),
        ScheduleDefinition(
            job=update_tickers_job,
            cron_schedule="0 23 * * *",
            execution_timezone="America/New_York"
        )
    ]
