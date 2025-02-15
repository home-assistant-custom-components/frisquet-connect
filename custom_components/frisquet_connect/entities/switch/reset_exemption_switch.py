import logging

from homeassistant.const import STATE_OFF, STATE_ON

from custom_components.frisquet_connect.const import SWITCH_EXEMPTION_TRANSLATIONS_KEY, ZoneSelector
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.entities.switch.core_reset_switch import CoreResetSwitch
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class ResetExemptionSwitchEntity(CoreResetSwitch):
    _zone_label_id: str

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, SWITCH_EXEMPTION_TRANSLATIONS_KEY)

        self._zone_label_id = zone_label_id
        self.auto_define_availability()

    @property
    def zone(self) -> Zone:
        return self.coordinator_typed.site.get_zone_by_label_id(self._zone_label_id)

    # @property
    # def icon(self) -> str | None:
    #     return "mdi:home-import-outline" if self._attr_state == STATE_ON else "mdi:home-export-outline"

    def auto_define_availability(self):
        self._attr_available = (
            self.zone.detail.selector == ZoneSelector.AUTO and self.zone.detail.is_exemption_enabled == True
        )

    async def async_update(self):
        self._attr_is_on = self.zone.detail.is_exemption_enabled == True
        self._attr_state = STATE_ON if self.zone.detail.is_exemption_enabled == True else STATE_OFF
        self.auto_define_availability()
