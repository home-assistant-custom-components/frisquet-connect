import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect.core_setup_entity import async_initialize_entity
from custom_components.frisquet_connect.entities.datetime.last_update import LastUpdateEntity
from datetime import timedelta

SCAN_INTERVAL = timedelta(seconds=150)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    (initialization_success, coordinator) = await async_initialize_entity(hass, entry, __name__)
    if not initialization_success:
        async_add_entities([], update_before_add=True)
        return

    _LOGGER.debug("1 entity/entities initialized")

    async_add_entities([LastUpdateEntity(coordinator)], update_before_add=True)
