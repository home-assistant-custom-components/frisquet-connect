from custom_components.frisquet_connect.const import (
    SENSOR_OUTSIDE_THERMOMETER_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.entities.sensor.core_thermometer import (
    CoreThermometer,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


class OutsideThermometerEntity(CoreThermometer):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator, SENSOR_OUTSIDE_THERMOMETER_TRANSLATIONS_KEY)

    async def async_update(self) -> None:
        self._attr_native_value = self.coordinator.data.external_temperature
