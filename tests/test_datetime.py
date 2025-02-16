from datetime import datetime
import pytest
from homeassistant.components.datetime import DateTimeEntity

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.datetime.boiler_datetime import BoilerDateTime
from custom_components.frisquet_connect.entities.datetime.last_update import LastUpdateEntity
from custom_components.frisquet_connect.datetime import async_setup_entry
from custom_components.frisquet_connect.const import (
    DOMAIN,
)
from custom_components.frisquet_connect.devices.frisquet_connect_device import (
    FrisquetConnectDevice,
)
from tests.conftest import async_core_setup_entry_with_site_id_mutated
from tests.utils import mock_endpoints, unstub_all


@pytest.mark.asyncio
async def test_async_setup_entry_success(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    # Initialize the mocks
    mock_endpoints()

    # Test the feature
    service = FrisquetConnectDevice(mock_entry.data.get("email"), mock_entry.data.get("password"))
    coordinator = FrisquetConnectCoordinator(mock_hass, service, mock_entry.data.get("site_id"))
    await coordinator._async_update()
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: coordinator}

    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]
    assert len(entities) == 2

    # Assertions
    for entity in entities:
        if not isinstance(entity, (DateTimeEntity)):
            assert False, f"Unknown entity type: {entity.__class__.__name__}"

        await entity.async_update()
        if isinstance(entity, LastUpdateEntity):
            entity: LastUpdateEntity
            assert entity.native_value == datetime(2025, 1, 31, 10, 0, 41)

        elif isinstance(entity, BoilerDateTime):
            entity: BoilerDateTime
            assert entity.native_value == datetime(2025, 1, 31, 10, 3, 40)

        else:
            assert False, f"Unknown entity type: {entity.__class__.__name__}"

    unstub_all()


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    await async_core_setup_entry_with_site_id_mutated(async_setup_entry, mock_add_entities, mock_hass, mock_entry)

    unstub_all()
