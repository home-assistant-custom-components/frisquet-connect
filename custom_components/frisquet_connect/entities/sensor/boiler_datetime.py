from homeassistant.components.sensor import SensorEntity, SensorDeviceClass


from custom_components.frisquet_connect.const import (
    SENSOR_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity
from homeassistant.core import callback


class BoilerDateTime(CoreEntity, SensorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)

        self._attr_unique_id = f"{self.coordinator.data.site_id}_{SENSOR_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY}"
        self._attr_translation_key = SENSOR_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY
        self._attr_device_class = SensorDeviceClass.DATE

    async def async_update(self) -> None:
        self._attr_native_value = self.coordinator.data.detail.current_boiler_timestamp

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_update()
