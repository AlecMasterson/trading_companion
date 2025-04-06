from typing import Any
from utils import LOGGER
import requests

def exchange(url: str, method: str, headers: dict = {}, params: dict = {}) -> Any:
    LOGGER.info(f"method={method} url={url} headers={headers} params={params}")
    response: requests.Response = requests.request(method, url, headers=headers, params=params)

    if response.status_code == requests.codes.ok:
        return response.json()

    raise Exception(f"<{response.status_code}> - {response.reason} - {response.text}")
