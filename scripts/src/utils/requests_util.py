from typing import Any
from utils import LOGGER
import requests


def get(url: str, headers: dict = {}, params: dict = {}) -> Any:
    """
    Function for making an HTTP GET request with proper error handling.
    An exception is thrown if an error occurs or the returned HTTP status is not OK.

    Parameters
    ----------
    url : str
        The URL to make the HTTP request against.
    headers : dict
        Dictionary (optional) containing header information for the HTTP request.
    params : dict
        Dictionary (optional) containing query parameter information for the HTTP request.

    Returns
    -------
    Any - A deserialized JSON response.
    """
    try:
        LOGGER.info(f"[HTTP] - url={url}, headers={headers}, params={params}")
        response: requests.Response = requests.get(url, headers=headers, params=params)

        # Return the JSON deserialized response ONLY if the HTTP status was okay.
        if response.status_code == requests.codes.ok:
            return response.json()

        raise Exception(f"<{response.status_code}> - {response.reason}")
    except Exception as e:
        raise Exception(f"[HTTP] - Failed to GET, {e}")
