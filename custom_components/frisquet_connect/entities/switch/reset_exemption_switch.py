import logging


from custom_components.frisquet_connect.const import SWITCH_EXEMPTION_TRANSLATIONS_KEY
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

    @property
    def zone(self) -> Zone:
        return self.coordinator_typed.site.get_zone_by_label_id(self._zone_label_id)

    @property
    def icon(self) -> str | None:
        return "mdi:home-import-outline" if self._attr_state == True else "mdi:home-export-outline"

    async def async_update(self):
        self._attr_is_on = self.zone.detail.is_exemption_enabled == True
