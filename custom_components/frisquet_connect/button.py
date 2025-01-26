import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from datetime import timedelta

from custom_components.frisquet_connect.const import DOMAIN
from custom_components.frisquet_connect.entities.button.reset_boost_button import ResetBoostButtonEntity
from custom_components.frisquet_connect.entities.button.reset_exemption_button import ResetExemptionButtonEntity
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator
from custom_components.frisquet_connect.services.frisquet_connect_service import FrisquetConnectService

SCAN_INTERVAL = timedelta(seconds=150)

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    service: FrisquetConnectService = hass.data[DOMAIN][entry.unique_id]
    coordinator = FrisquetConnectCoordinator(hass, service)

    entities = []

    # Exemption are for all zones, so keep only the first one
    if len(coordinator.site.zones) > 0:
        entity = ResetExemptionButtonEntity(coordinator, coordinator.site.zones[0].label_id)
        entities.append(entity)

    # Boost are for each zone
    for zone in coordinator.site.zones:
        entity = ResetBoostButtonEntity(coordinator, zone.label_id)
        entities.append(entity)

    async_add_entities(entities, update_before_add=False)
