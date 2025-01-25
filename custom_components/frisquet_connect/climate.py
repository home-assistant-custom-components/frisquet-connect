from custom_components.frisquet_connect.const import DOMAIN
from custom_components.frisquet_connect.entities.climate.frisquet_connect_entity import FrisquetConnectEntity
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator
from custom_components.frisquet_connect.services.frisquet_connect_service import FrisquetConnectService
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback


LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    service: FrisquetConnectService = hass.data[DOMAIN][entry.unique_id]
    coordinator = FrisquetConnectCoordinator(hass, service)

    entites = []
    for zone in coordinator.site.zones:
        entity = FrisquetConnectEntity(coordinator, zone.label_id)
        entites.append(entity)

    async_add_entities(entites, update_before_add=False)
