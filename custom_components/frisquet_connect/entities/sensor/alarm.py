import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import (
    SENSOR_ALARM_TRANSLATIONS_KEY,
    AlarmType,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/core/entity/sensor/
class AlarmEntity(SensorEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating Alarm entity")

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}_{SENSOR_ALARM_TRANSLATIONS_KEY}"
        self._attr_translation_key = SENSOR_ALARM_TRANSLATIONS_KEY
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [alarm_type for alarm_type in AlarmType]

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    @property
    def device_info(self):
        return get_device_info(self.name, self.unique_id, self.coordinator_typed)

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    async def async_update(self):
        value: str = AlarmType.NO_ALARM
        for alarm in self.coordinator_typed.site.alarms:
            # TODO: Handle multiple alarms
            value = alarm.alarme_type
            break

        self._attr_native_value = value
