import logging
from homeassistant.components.sensor import SensorEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect_unofficial.const import ALARM_CARD_NAME, NO_ALARM, AlarmType
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class AlarmEntity(SensorEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)

        self._attr_unique_id = f"{coordinator.site.site_id}-alert"
        self._attr_name = ALARM_CARD_NAME

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
