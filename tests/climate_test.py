import os
from aiohttp import ClientSession
import dotenv
from mockito import patch
import pytest
from unittest.mock import AsyncMock
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect_unofficial.climate import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from custom_components.frisquet_connect_unofficial.entities.climate.default_climate import DefaultClimateEntity
from tests.utils import read_json_file

dotenv.load_dotenv()


@pytest.fixture
def mock_hass():
    mock = AsyncMock(spec=HomeAssistant)
    mock.data = {}
    return mock


@pytest.fixture
def mock_entry():
    mock_entry_file = read_json_file("mock_entry.json")
    mock = AsyncMock(spec=ConfigEntry)
    mock.data = mock_entry_file.get("data")
    mock.unique_id = mock_entry_file.get("unique_id")

    # Use environment variables if available to override the mock data
    if os.getenv("EMAIL") and os.getenv("PASSWORD") and os.getenv("SITE_ID"):
        mock.data["email"] = os.getenv("EMAIL")
        mock.data["password"] = os.getenv("PASSWORD")
        mock.data["site_id"] = os.getenv("SITE_ID")

    return mock


@pytest.fixture
def mock_add_entities():
    return AsyncMock(spec=AddEntitiesCallback)


# TODO : Continue the implementation of the test
def mock_repository_authentication_endpoint():
    # TODO: Read json file
    mock_response = {
        "status": "success",
        "data": {
            "site": {
                "name": "Site de test",
                "zones": [{"label_id": "Z1", "name": "Zone 1"}, {"label_id": "Z2", "name": "Zone 2"}],
            }
        },
    }

    async def mock_get(*args, **kwargs):
        class MockResponse:
            async def json(self):
                return mock_response

        return MockResponse()

    patcher = patch.object(ClientSession, "get", new=mock_get)
    patcher.start()


@pytest.mark.asyncio
async def test_async_setup_entry_success(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    service = FrisquetConnectService(mock_entry)
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: service}
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
    mock_entry.data = {"site_id ": None}

    service = FrisquetConnectService(mock_entry)
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: service}
    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]
    assert len(entities) == 0
