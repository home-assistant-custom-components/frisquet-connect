from custom_components.entities.sensor.core_thermometer import CoreThermometer
from custom_components.frisquet_connect.const import OUTSIDE_THERMOMETER_LABEL
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator


class OutsideThermoeterEntity(CoreThermometer):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator, "outside", OUTSIDE_THERMOMETER_LABEL)

    async def async_update(self):
        self._attr_native_value = self._site.external_temperature
