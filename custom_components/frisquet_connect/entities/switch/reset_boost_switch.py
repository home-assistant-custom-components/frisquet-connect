import logging

from custom_components.frisquet_connect.const import SWITCH_BOOST_TRANSLATIONS_KEY
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.entities.switch.core_reset_switch import CoreResetSwitch
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class ResetBoostSwitchEntity(CoreResetSwitch):
    _zone_label_id: str

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, SWITCH_BOOST_TRANSLATIONS_KEY, zone_label_id)

        self._zone_label_id = zone_label_id
        self._attr_translation_placeholders = {"zone_name": self.zone.name}

    @property
    def zone(self) -> Zone:
        return self.coordinator_typed.site.get_zone_by_label_id(self._zone_label_id)

    @property
    def icon(self) -> str | None:
        return "mdi:heat-wave"

    async def async_update(self):
        self._attr_is_on = self.zone.detail.is_boosting == True
