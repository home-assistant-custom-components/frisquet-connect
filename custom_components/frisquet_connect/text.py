from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.entities.text.alarm import AlarmEntity
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator
from custom_components.frisquet_connect.services.frisquet_connect_service import FrisquetConnectService
from .const import DOMAIN

from datetime import timedelta

SCAN_INTERVAL = timedelta(seconds=150)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    service: FrisquetConnectService = hass.data[DOMAIN][entry.unique_id]
    site_id = entry.data.get("site_id")

    coordinator = FrisquetConnectCoordinator(hass, service)
    entity = AlarmEntity(coordinator)
    entites = [entity]

    async_add_entities(entites, update_before_add=False)
