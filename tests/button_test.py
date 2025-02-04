import os
import pytest
from unittest.mock import AsyncMock
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_OFF
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect_unofficial.button import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.entities.button.core_reset_button import CoreResetButton
from custom_components.frisquet_connect_unofficial.entities.button.reset_boost_button import ResetBoostButtonEntity
from custom_components.frisquet_connect_unofficial.entities.button.reset_exemption_button import (
    ResetExemptionButtonEntity,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
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
    if os.getenv("EMAIL") and os.getenv("PASSWORD") and os.getenv("SITE_ID"):
        mock.data["email"] = os.getenv("EMAIL")
        mock.data["password"] = os.getenv("PASSWORD")
        mock.data["site_id"] = os.getenv("SITE_ID")

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
    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]
    assert len(entities) == 2

    for entity in entities:
        if not isinstance(entity, CoreResetButton):
            assert False, f"Unknown entity type: {entity.__class__.__name__}"

        await entity.async_update()

        if isinstance(entity, ResetBoostButtonEntity):
            entity: ResetBoostButtonEntity
            assert entity._zone.label_id == "Z1"
            assert entity._attr_state == STATE_OFF

        elif isinstance(entity, ResetExemptionButtonEntity):
            entity: ResetExemptionButtonEntity
            assert entity._attr_state == STATE_OFF

        else:
            assert False, f"Unknown entity type: {entity.__class__.__name__}"


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    async_core_setup_entry_no_site_id(async_setup_entry, mock_hass, mock_entry, mock_add_entities)
