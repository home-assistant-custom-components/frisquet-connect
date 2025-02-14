import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import (
    SENSOR_ALARM_TRANSLATIONS_KEY,
    NO_ALARM,
    AlarmType,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.utils import get_device_info


_LOGGER = logging.getLogger(__name__)


class AlarmEntity(SensorEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating Alarm entity")

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}-{SENSOR_ALARM_TRANSLATIONS_KEY}"
        self._attr_translation_key = SENSOR_ALARM_TRANSLATIONS_KEY
        self._attr_options = [alarm_type.name for alarm_type in AlarmType]

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.name, self.unique_id, self.coordinator)

    @property
    def icon(self) -> str | None:
        return "mdi:alert"

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    async def async_update(self):
        self._attr_state = AlarmType
        value: str = NO_ALARM
        state: str
        for alarm in self.coordinator_typed.site.alarms:
            value = alarm.description
            state = alarm.alarme_type.name

        self._attr_native_value = value
        self._attr_state = state
