import logging
import requests

from custom_components.frisquet_connect.domains.exceptions import CallApiException, ForbiddenAccessException


LOGGER = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "Frisquet%20Connect/16 CFNetwork/974.2.1 Darwin/18.0.0"


async def _call_api(url, method: str, data_json: dict = None, params: dict = None):
    """
    Makes an HTTP request to the specified URL using the given method and data.
    Args:
        url (str): The URL to which the request is to be made.
        method (str, optional): The HTTP method to use for the request. Defaults to "GET".
        data (dict, optional): The data to send with the request, if applicable. Defaults to None.
    Returns:
        requests.Response: The response object resulting from the HTTP request.
    """
    LOGGER.debug(f"Calling API: {url}")
    headers = {"Content-Type": "application/json", "User-Agent": DEFAULT_USER_AGENT}

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data_json)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data_json)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response
    except requests.RequestException as e:
        error_message = f"API call failed: {e}"
        class_exception = CallApiException

        if e.response is not None:
            error_message = f"API call failed: {e.response.status_code} - {e.response.text}"
            if e.response.status_code == 403:
                class_exception = ForbiddenAccessException

        LOGGER.error(error_message)
        raise class_exception(error_message)


async def do_get(url: str, params: dict):
    return await _call_api(url, "GET", None, params).json()


async def do_post(url: str, data: dict):
    return await _call_api(url, "POST", data).json()
