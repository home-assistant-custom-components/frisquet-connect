import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect_unofficial.core_setup_entity import async_initialize_entity
from custom_components.frisquet_connect_unofficial.entities.switch.core_reset_switch import (
    CoreResetSwitch,
)
from custom_components.frisquet_connect_unofficial.entities.switch.reset_boost_switch import (
    ResetBoostSwitchEntity,
)
from custom_components.frisquet_connect_unofficial.entities.switch.reset_exemption_switch import (
    ResetExemptionSwitchEntity,
)

SCAN_INTERVAL = timedelta(seconds=150)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    (initialization_success, coordinator) = await async_initialize_entity(hass, entry, __name__)
    if not initialization_success:
        async_add_entities([], update_before_add=False)
        return

    entities: list[CoreResetSwitch] = []

    # Exemption are for all zones, so keep only the first one
    if len(coordinator.site.zones) > 0:
        entity = ResetExemptionSwitchEntity(coordinator, coordinator.site.zones[0].label_id)
        entities.append(entity)

    # Boost are for each zone
    for zone in coordinator.site.zones:
        entity = ResetBoostSwitchEntity(coordinator, zone.label_id)
        entities.append(entity)

    _LOGGER.debug(f"{len(entities)} entity/entities initialized")

    async_add_entities(entities, update_before_add=False)
