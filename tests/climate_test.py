import json
import aiohttp
import pytest
from mockito import contains, when, ANY
from unittest.mock import AsyncMock
from tests.utils import read_json_file_as_json, read_json_file_as_text


import os
import pytest
from unittest.mock import AsyncMock
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect_unofficial.climate import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.climate.default_climate import DefaultClimateEntity
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from custom_components.frisquet_connect_unofficial.repositories.frisquet_connect_repository import (
    AUTH_ENDPOINT,
    SITES_ENDPOINT,
)
from tests.core_setup_entry import async_core_setup_entry_no_site_id
from tests.utils import read_json_file_as_json


@pytest.fixture
def mock_hass():
    mock = AsyncMock(spec=HomeAssistant)
    mock.data = {}
    return mock


@pytest.fixture
def mock_entry():
    mock_entry_file = read_json_file_as_json("mock_entry")
    mock = AsyncMock(spec=ConfigEntry)
    mock.data = mock_entry_file.get("data")
    mock.unique_id = mock_entry_file.get("unique_id")

    # Use environment variables if available to override the mock data
    # if os.getenv("EMAIL") and os.getenv("PASSWORD") and os.getenv("SITE_ID"):
    #     mock.data["email"] = os.getenv("EMAIL")
    #     mock.data["password"] = os.getenv("PASSWORD")
    #     mock.data["site_id"] = os.getenv("SITE_ID")

    return mock


@pytest.fixture
def mock_add_entities():
    return AsyncMock(spec=AddEntitiesCallback)


@pytest.mark.asyncio
async def test_async_setup_entry_success(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    service = FrisquetConnectService(mock_entry)
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: service}
    mock_authentication_endpoint()
    mock_sites_endpoints()
    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]
    assert len(entities) == 1
    assert isinstance(entities[0], DefaultClimateEntity)

    entity: DefaultClimateEntity = entities[0]
    zone: Zone = entity._zone
    assert zone is not None
    assert entity._zone.label_id == "Z1"

    if os.getenv("SITE_ID") is None:
        site: Site = entity.coordinator_typed.site
        assert site is not None
        assert site.name == "Site de test"

        # TODO: Add more assertions here with the data mocked in the test


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    async_core_setup_entry_no_site_id(async_setup_entry, mock_hass, mock_entry, mock_add_entities)


# TODO: review all below but work
AsyncMock.__await__ = lambda x: async_magic(x).__await__()


async def async_magic(x):
    return x


def mock_sites_endpoints() -> None:
    class MockResponse(AsyncMock):
        def __init__(self, text, status):
            super().__init__()
            self._text = text
            self.status = status

        async def json(self):
            return json.loads(self._text)

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def __aenter__(self):
            return self

    mock = MockResponse(read_json_file_as_text("sites"), 200)
    when(aiohttp.ClientSession).get(contains(SITES_ENDPOINT), params=ANY).thenReturn(mock)


def mock_authentication_endpoint() -> None:
    authentication_json = read_json_file_as_json("authentication")
    when(aiohttp.ClientSession).post(contains(AUTH_ENDPOINT), headers=ANY, json=ANY).thenReturn(authentication_json)
