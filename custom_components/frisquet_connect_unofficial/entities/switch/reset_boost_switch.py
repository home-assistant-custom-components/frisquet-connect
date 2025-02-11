import logging

from custom_components.frisquet_connect_unofficial.const import BOOST_SWITCH_TRANSLATIONS_KEY
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.switch.core_reset_switch import CoreResetSwitch
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class ResetBoostSwitchEntity(CoreResetSwitch):
    _zone: Zone

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, BOOST_SWITCH_TRANSLATIONS_KEY, zone_label_id)

        self._zone = coordinator.site.get_zone_by_label_id(zone_label_id)
        self._attr_translation_placeholders = {"zone_name": self._zone.name}

    @property
    def icon(self) -> str | None:
        return "mdi:heat-wave"

    async def async_update(self):
        self._attr_is_on = self._zone.detail.is_boosting
