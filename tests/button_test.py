import pytest
from unittest.mock import AsyncMock
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
from tests.core_setup_entry import async_core_setup_entry_no_site_id
from tests.utils import mock_endpoints, mock_entry, mock_hass


@pytest.fixture
def mock_add_entities():
    return AsyncMock(spec=AddEntitiesCallback)


@pytest.mark.asyncio
async def test_async_setup_entry_success(mock_add_entities: AddEntitiesCallback):
    # Initialize the mocks
    mock_endpoints()
    hass = mock_hass()
    entry = mock_entry()

    # Test the feature
    service = FrisquetConnectService(entry)
    hass.data[DOMAIN] = {entry.unique_id: service}
    await async_setup_entry(hass, entry, mock_add_entities)

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
async def test_async_setup_entry_no_site_id(mock_add_entities: AddEntitiesCallback):
    async_core_setup_entry_no_site_id(async_setup_entry, mock_add_entities)
