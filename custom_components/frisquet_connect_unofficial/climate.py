from custom_components.frisquet_connect_unofficial.core_setup_entity import async_initialize_entity
from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.entities.climate.default_climate import DefaultClimateEntity
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback


LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    (initialization_success, coordinator) = await async_initialize_entity(hass, entry)
    if not initialization_success:
        async_add_entities([], update_before_add=False)
        return

    entities: list[DefaultClimateEntity] = []
    for zone in coordinator.site.zones:
        entity = DefaultClimateEntity(coordinator, zone.label_id)
        entities.append(entity)

    async_add_entities(entities, update_before_add=False)
