import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect.core_setup_entity import async_initialize_entity
from custom_components.frisquet_connect.entities.button.refresh_data import (
    RefreshDataButton,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    initialization_success, coordinator = await async_initialize_entity(hass, entry, __name__)
    if not initialization_success:
        async_add_entities([], update_before_add=True)
        return

    entities = [RefreshDataButton(coordinator)]
    _LOGGER.debug("%d button entity initialized", len(entities))
    async_add_entities(entities, update_before_add=True)
