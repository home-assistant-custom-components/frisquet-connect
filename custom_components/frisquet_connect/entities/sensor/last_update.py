from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import (
    SENSOR_BOILER_LAST_UPDATE_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity


class LastUpdateEntity(SensorEntity, CoordinatorEntity, CoreEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        CoreEntity.__init__(self)

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}_{SENSOR_BOILER_LAST_UPDATE_TRANSLATIONS_KEY}"
        self._attr_translation_key = SENSOR_BOILER_LAST_UPDATE_TRANSLATIONS_KEY
        self._attr_device_class = SensorDeviceClass.DATE

    async def async_update(self):
        self._attr_native_value = self.coordinator_typed.site.last_updated

    @property
    def should_poll(self) -> bool:
        return True
