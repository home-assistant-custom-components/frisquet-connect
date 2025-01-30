from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.entities.climate.default_climate import DefaultClimateEntity
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback


LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    service: FrisquetConnectService = hass.data[DOMAIN][entry.unique_id]
    coordinator = FrisquetConnectCoordinator(hass, service, entry.data["site_id"])
    await coordinator._async_update()

    entites = []
    for zone in coordinator.site.zones:
        entity = DefaultClimateEntity(coordinator, zone.label_id)
        entites.append(entity)

    async_add_entities(entites, update_before_add=False)
