from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.download_ticker_history import main
from src.enums.Source import Source

with DAG(
    "download_ticker_history_v01",
    catchup=False,
    schedule_interval="@hourly",
    start_date=datetime(2022, 1, 1)
) as dag:
    task_download_tickers = PythonOperator(
        task_id="download_ticker_history",
        python_callable=main,
        op_kwargs={"source": Source.COINBASE, "ticker": "BTC-USD"}
    )
