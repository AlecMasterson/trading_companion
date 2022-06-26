from typing import Any, List, Optional
from utils import LOGGER
import requests

HEADERS_DEFAULT = {"Accept": "application/json"}

def get(url: str) -> Optional[List[Any]]:
    """
    Function for making HTTP GET requests with proper error handling.
    An exception is thrown if an HTTP error occurs during API call.

    Parameters:
        - url [str] - the URL to make the HTTP request against

    Returns:
        Optional[List[Any]] - deserialized JSON response from request
    """
    try:
        LOGGER.info(f"[HTTP-GET] - {url}")
        response: requests.Response = requests.get(url, headers=HEADERS_DEFAULT)

        # Return the JSON deserialized response ONLY if the HTTP status was okay.
        if response.status_code == requests.codes.ok:
            return response.json()

        LOGGER.error(f"<HTTP: {response.status_code}> {response.reason}")
    except Exception as e:
        LOGGER.error(e)

    return None
