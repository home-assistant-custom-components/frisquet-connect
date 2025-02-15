import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import (
    SENSOR_LAST_UPDATE_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


_LOGGER = logging.getLogger(__name__)


class LastUpdateEntity(SensorEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating Alarm entity")

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}_{SENSOR_LAST_UPDATE_TRANSLATIONS_KEY}"
        self._attr_translation_key = SENSOR_LAST_UPDATE_TRANSLATIONS_KEY
        self._attr_device_class = SensorDeviceClass.DATE

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    async def async_update(self):
        self._attr_native_value = self.coordinator_typed.site.last_updated
