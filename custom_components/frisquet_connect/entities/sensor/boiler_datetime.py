from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import (
    SENSOR_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity
from homeassistant.core import callback


class BoilerDateTime(SensorEntity, CoordinatorEntity, CoreEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        CoreEntity.__init__(self)

        self._attr_unique_id = (
            f"{self.coordinator_typed.site.site_id}_{SENSOR_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY}"
        )
        self._attr_translation_key = SENSOR_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY
        self._attr_device_class = SensorDeviceClass.DATE

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator_typed.site.detail.current_boiler_timestamp

        self.async_write_ha_state()
