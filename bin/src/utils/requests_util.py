from typing import Any
from utils import LOGGER
import requests


def exchange(url: str, method: str, headers: dict = {}, params: dict = {}) -> Any:
    """
    Function for making an HTTP request with proper error handling.
    An exception is thrown if an error occurs or the returned HTTP status is not OK.

    Parameters
    ----------
    url : str
        The URL to make the HTTP request against.
    method : str
        Type of HTTP request (GET, POST, etc).
    headers : dict (optional)
        Header information to include in the HTTP request.
    params : dict (optional)
        Query parameters to include in the HTTP request.

    Returns
    -------
    Any - A deserialized JSON response.
    """
    try:
        LOGGER.info(f"[HTTP] - [{method}] - url={url}, headers={headers}, params={params}")
        response: requests.Response = requests.request(url, headers=headers, method=method, params=params)

        # Return the deserialized JSON response if the HTTP status was okay.
        if response.status_code == requests.codes.ok:
            return response.json()

        raise Exception(f"<{response.status_code}> - {response.reason} - {response.text}")
    except Exception as e:
        raise Exception(f"[HTTP] - [{method}] - Failed, {e}")
