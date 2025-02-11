import logging

from homeassistant.const import STATE_ON, STATE_OFF
from custom_components.frisquet_connect_unofficial.const import BOOST_BUTTON_TRANSLATIONS_KEY
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.button.core_reset_button import (
    CoreResetButton,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class ResetBoostButtonEntity(CoreResetButton):
    _zone: Zone

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, BOOST_BUTTON_TRANSLATIONS_KEY, zone_label_id)

        self._zone = coordinator.site.get_zone_by_label_id(zone_label_id)
        self._attr_translation_placeholders = {"zone_name": self._zone.name}

    @property
    def icon(self) -> str | None:
        return "mdi:heat-wave"

    async def async_update(self):
        self._attr_state = STATE_ON if self._zone.detail.is_boosting else STATE_OFF
