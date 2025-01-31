import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.entities.sensor.alarm import AlarmEntity
from custom_components.frisquet_connect_unofficial.entities.sensor.core_consumption import CoreConsumption
from custom_components.frisquet_connect_unofficial.entities.sensor.core_thermometer import CoreThermometer
from custom_components.frisquet_connect_unofficial.entities.sensor.heating_consumption import HeatingConsumptionEntity
from custom_components.frisquet_connect_unofficial.entities.sensor.inside_thermometer import InsideThermoeterEntity
from custom_components.frisquet_connect_unofficial.entities.sensor.outside_thermometer import OutsideThermoeterEntity
from custom_components.frisquet_connect_unofficial.entities.sensor.sanitary_consumption import (
    SanitaryConsumptionEntity,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService

from datetime import timedelta

SCAN_INTERVAL = timedelta(seconds=150)

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    service: FrisquetConnectService = hass.data[DOMAIN][entry.unique_id]
    coordinator = FrisquetConnectCoordinator(hass, service)

    if not coordinator.is_site_loaded:
        LOGGER.error("Site not found")
        return

    entities: list[CoreConsumption | CoreThermometer | AlarmEntity] = [
        SanitaryConsumptionEntity(coordinator),
        HeatingConsumptionEntity(coordinator),
        OutsideThermoeterEntity(coordinator),
        AlarmEntity(coordinator),
    ]
    for zone in coordinator.site.zones:
        entity = InsideThermoeterEntity(coordinator, zone.label_id)
        entities.append(entity)

    async_add_entities(entities, update_before_add=False)
