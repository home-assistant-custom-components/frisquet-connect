import logging
from homeassistant.components.sensor import SensorEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import ALARM_CARD_NAME, NO_ALARM, AlarmType
from custom_components.frisquet_connect.domains.site.site import Site
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator


LOGGER = logging.getLogger(__name__)


class AlarmEntity(SensorEntity, CoordinatorEntity):
    _site: Site

    def __init__(self, coordinator: FrisquetConnectCoordinator, idx) -> None:
        super().__init__(coordinator)

        self._site = coordinator.site
        self._attr_unique_id = f"{self._site.site_id}-alert"
        self._attr_name = ALARM_CARD_NAME

    @property
    def icon(self) -> str | None:
        return "mdi:alert"

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    async def async_update(self):
        self._attr_state = AlarmType
        value: str = NO_ALARM
        state: str
        for alarm in self._site.alarms:
            value = alarm.description
            state = alarm.alarme_type.name

        self._attr_native_value = value
        self._attr_state = state
