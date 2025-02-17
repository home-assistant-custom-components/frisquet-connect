import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import SENSOR_HEATING_CONSUMPTION_TRANSLATIONS_KEY, ConsumptionType
from custom_components.frisquet_connect.entities.sensor.core_consumption import (
    CoreConsumption,
)


LOGGER = logging.getLogger(__name__)


class HeatingConsumptionEntity(CoreConsumption):

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator, SENSOR_HEATING_CONSUMPTION_TRANSLATIONS_KEY)
        self._consumption_type = ConsumptionType.HEATING
