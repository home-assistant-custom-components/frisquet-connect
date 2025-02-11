import logging

from homeassistant.const import STATE_ON, STATE_OFF

from custom_components.frisquet_connect_unofficial.const import EXEMPTION_BUTTON_TRANSLATIONS_KEY
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.button.core_reset_button import (
    CoreResetSwitch,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class ResetExemptionSwitchEntity(CoreResetSwitch):
    _zone: Zone

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, EXEMPTION_BUTTON_TRANSLATIONS_KEY)

        self._zone = coordinator.site.get_zone_by_label_id(zone_label_id)

    @property
    def icon(self) -> str | None:
        return "mdi:home-import-outline" if self._attr_state == STATE_ON else "mdi:home-export-outline"

    async def async_update(self):
        self._attr_is_on = STATE_ON if self._zone.detail.is_exemption_enabled else STATE_OFF
