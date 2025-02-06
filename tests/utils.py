import json
import aiohttp

from mockito import contains, unstub, when, ANY
from custom_components.frisquet_connect_unofficial.repositories.frisquet_connect_repository import (
    AUTH_ENDPOINT,
    SITES_ENDPOINT,
)
from unittest.mock import AsyncMock, Mock

RESOURCES_PATH = "./tests/resources"


#
# Utils mocks
#
AsyncMock.__await__ = lambda x: async_magic(x).__await__()


async def async_magic(x):
    return x


class MockResponse(AsyncMock):
    def __init__(self, text, status):
        super().__init__()
        self._text = text
        self.status = status

    def raise_for_status(self):
        if self.status != 200:
            raise aiohttp.ClientResponseError(request_info=Mock(), history=[], status=self.status, message=self._text)

    async def json(self):
        return json.loads(self._text)

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


#
# Mocks
#
def mock_endpoints() -> None:
    mock_authentication_endpoint()
    mock_sites_endpoint_with_forbidden()
    mock_sites_endpoint_not_found()
    mock_sites_endpoint()


def mock_authentication_endpoint() -> None:
    mock = MockResponse(read_json_file_as_text("authentication"), 200)
    when(aiohttp.ClientSession).post(contains(AUTH_ENDPOINT), headers=ANY, json=ANY).thenReturn(mock)


def mock_sites_endpoint_with_forbidden() -> None:
    mock = MockResponse('{"message": "Echec d\'authentification"}', 403)
    mock_params = {"token": ""}
    when(aiohttp.ClientSession).get(contains(f"{SITES_ENDPOINT}/12345678901234"), params=mock_params).thenReturn(mock)


def mock_sites_endpoint() -> None:
    mock = MockResponse(read_json_file_as_text("sites"), 200)
    mock_params = {"token": "00000000000000000000000000000000"}
    when(aiohttp.ClientSession).get(contains(f"{SITES_ENDPOINT}/12345678901234"), params=mock_params).thenReturn(mock)


def mock_sites_endpoint_not_found() -> None:
    mock = MockResponse('{"code": 404, "message": "Not Found" }', 404)
    mock_params = {"token": "00000000000000000000000000000000"}
    when(aiohttp.ClientSession).get(contains(f"{SITES_ENDPOINT}/not_found"), params=mock_params).thenReturn(mock)


def unstub_all():
    unstub()


#
# Read content of a file
#
def read_json_file_as_json(file_path) -> dict:
    return json.loads(read_json_file_as_text(file_path))


def read_json_file_as_text(file_path) -> str:
    with open(f"{RESOURCES_PATH}/{file_path}.json", "r", encoding="utf-8") as file:
        return file.read()
