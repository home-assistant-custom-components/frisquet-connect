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
from custom_components.frisquet_connect.entities.core_entity import CoreEntity
from custom_components.frisquet_connect.utils import log_methods


_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/core/entity/sensor/
@log_methods
class AlarmEntity(SensorEntity, CoordinatorEntity, CoreEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        CoreEntity.__init__(self)

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}_{SENSOR_ALARM_TRANSLATIONS_KEY}"
        self._attr_translation_key = SENSOR_ALARM_TRANSLATIONS_KEY
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [alarm_type for alarm_type in AlarmType]

    async def async_update(self):
        value: str = AlarmType.NO_ALARM
        for alarm in self.coordinator_typed.site.alarms:
            # TODO: Handle multiple alarms
            value = alarm.alarme_type
            break

        self._attr_native_value = value
