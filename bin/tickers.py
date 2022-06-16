from conf import LOGGER
from type.Source import Source
from typing import Any, List
import requests

URL_TICKERS = {
    Source.BINANCE: "",
    Source.COINBASE: "https://api.exchange.coinbase.com/productss"
}

def download_tickers(source: Source) -> List[Any] or None:
    """
    Function for downloading the available tickers from the given source.
    An exception is thrown if an HTTP error occurs during API call.

    Parameters:
    source [Source] - where the available tickers will be queried from

    Returns:
    List[Any] (or None) - API response containing list of tickers in the given source format
    """
    try:
        response: requests.Response = requests.get(URL_TICKERS[source], headers={"Accept": "application/json"})

        # Return the JSON deserialized response ONLY if the HTTP status was okay.
        if response.status_code == requests.codes.ok:
            return response.json()

        LOGGER.error(f"(source: {source}), <HTTP: {response.status_code}> - {response.reason}")
    except Exception as e:
        LOGGER.error(f"(source: {source}), {e}")
    finally:
        return None

def update_active_tickers(ti: Any) -> None:
    products = ti.xcom_pull(task_id="download_tickers")
