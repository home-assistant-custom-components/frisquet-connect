import pytest

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect_unofficial.button import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.entities.button.core_reset_button import CoreResetButton
from custom_components.frisquet_connect_unofficial.entities.button.reset_boost_button import ResetBoostButtonEntity
from custom_components.frisquet_connect_unofficial.entities.button.reset_exemption_button import (
    ResetExemptionButtonEntity,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from tests.conftest import async_core_setup_entry_no_site_id
from tests.utils import mock_endpoints


@pytest.mark.asyncio
async def test_async_setup_entry_success(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    # Initialize the mocks
    mock_endpoints()

    # Test the feature
    service = FrisquetConnectService(mock_entry)
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: service}
    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]
    assert len(entities) == 2

    # Assertions
    for entity in entities:
        if not isinstance(entity, CoreResetButton):
            assert False, f"Unknown entity type: {entity.__class__.__name__}"

        await entity.async_update()

        if isinstance(entity, ResetBoostButtonEntity):
            entity: ResetBoostButtonEntity
            assert entity._zone.label_id == "Z1"
            assert entity._attr_state == STATE_OFF

            # TODO : test the action to reset

        elif isinstance(entity, ResetExemptionButtonEntity):
            entity: ResetExemptionButtonEntity
            assert entity._attr_state == STATE_ON

            # TODO : test the action to reset

        else:
            assert False, f"Unknown entity type: {entity.__class__.__name__}"


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    await async_core_setup_entry_no_site_id(async_setup_entry, mock_add_entities, mock_hass, mock_entry)
