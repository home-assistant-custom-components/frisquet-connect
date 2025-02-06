import logging
import aiohttp
from custom_components.frisquet_connect_unofficial.domains.exceptions.call_api_exception import CallApiException
from custom_components.frisquet_connect_unofficial.domains.exceptions.forbidden_access_exception import (
    ForbiddenAccessException,
)


LOGGER = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "Frisquet%20Connect/16 CFNetwork/974.2.1 Darwin/18.0.0"


async def _async_call_api(url, method: str, params: dict = None, data_json: dict = None) -> dict:
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
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            if method == "GET":
                response = await session.get(url, headers=headers, params=params)
            elif method == "POST":
                response = await session.post(url, headers=headers, params=params, json=data_json)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return await response.json()
        except aiohttp.ClientResponseError as e:
            error_message = f"API call failed: {e.status} - {e.message}"
            class_exception = CallApiException

            if e.status == 403:
                class_exception = ForbiddenAccessException

            LOGGER.error(error_message)
            raise class_exception(error_message)


async def async_do_get(url: str, params: dict) -> dict:
    return await _async_call_api(url, "GET", params)


async def async_do_post(url: str, params: dict, data: dict) -> dict:
    return await _async_call_api(url, "POST", params, data)
