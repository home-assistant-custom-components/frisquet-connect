import logging


from custom_components.frisquet_connect.const import SENSOR_HEATING_CONSUMPTION_TRANSLATIONS_KEY, ConsumptionType
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import FrisquetConnectCoordinator
from custom_components.frisquet_connect.entities.sensor.core_consumption import (
    CoreConsumption,
)


LOGGER = logging.getLogger(__name__)


class HeatingConsumptionEntity(CoreConsumption):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator, SENSOR_HEATING_CONSUMPTION_TRANSLATIONS_KEY)
        self._consumption_type = ConsumptionType.HEATING
