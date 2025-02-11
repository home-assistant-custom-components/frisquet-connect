import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect_unofficial.core_setup_entity import async_initialize_entity
from custom_components.frisquet_connect_unofficial.entities.button.core_reset_button import (
    CoreResetButton,
)
from custom_components.frisquet_connect_unofficial.entities.button.reset_boost_button import (
    ResetBoostButtonEntity,
)
from custom_components.frisquet_connect_unofficial.entities.button.reset_exemption_button import (
    ResetExemptionButtonEntity,
)

SCAN_INTERVAL = timedelta(seconds=150)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    (initialization_success, coordinator) = await async_initialize_entity(hass, entry, __name__)
    if not initialization_success:
        await async_add_entities([], update_before_add=False)
        return

    entities: list[CoreResetButton] = []

    # Exemption are for all zones, so keep only the first one
    if len(coordinator.site.zones) > 0:
        entity = ResetExemptionButtonEntity(coordinator, coordinator.site.zones[0].label_id)
        entities.append(entity)

    # Boost are for each zone
    for zone in coordinator.site.zones:
        entity = ResetBoostButtonEntity(coordinator, zone.label_id)
        entities.append(entity)

    _LOGGER.debug(f"{len(entities)} entity/entities initialized")

    await async_add_entities(entities, update_before_add=False)
