import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.core_setup_entity import async_initialize_entity
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
from datetime import timedelta

SCAN_INTERVAL = timedelta(seconds=150)

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    (initialization_success, coordinator) = await async_initialize_entity(hass, entry)
    if not initialization_success:
        async_add_entities([], update_before_add=False)
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
