import pytest

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.switch import async_setup_entry
from custom_components.frisquet_connect.const import DOMAIN
from custom_components.frisquet_connect.entities.switch.core_reset_switch import (
    CoreResetSwitch,
)
from custom_components.frisquet_connect.entities.switch.reset_boost_switch import (
    ResetBoostSwitchEntity,
)
from custom_components.frisquet_connect.entities.switch.reset_exemption_switch import (
    ResetExemptionSwitchEntity,
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
        if not isinstance(entity, CoreResetSwitch):
            assert False, f"Unknown entity type: {entity.__class__.__name__}"

        await entity.async_update()

        if isinstance(entity, ResetBoostSwitchEntity):
            entity: ResetBoostSwitchEntity
            assert entity.zone.label_id == "Z1"
            assert entity.is_on == False

            # TODO : test the action to reset

        elif isinstance(entity, ResetExemptionSwitchEntity):
            entity: ResetExemptionSwitchEntity
            assert entity.is_on == True

            # TODO : test the action to reset

        else:
            assert False, f"Unknown entity type: {entity.__class__.__name__}"

    unstub_all()


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    await async_core_setup_entry_with_site_id_mutated(async_setup_entry, mock_add_entities, mock_hass, mock_entry)

    unstub_all()
