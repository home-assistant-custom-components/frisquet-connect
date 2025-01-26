import logging

from custom_components.frisquet_connect.const import ButtonState, ExemptionButtonState
from custom_components.frisquet_connect.domains.site.site import Site
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.entities.button.core_reset_button import CoreResetButton
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator


LOGGER = logging.getLogger(__name__)


class ResetExemptionButtonEntity(CoreResetButton):
    _zone: Zone

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, f"exemption")

        self._zone = self._site.get_zone_by_label_id(zone_label_id)
        self._attr_name = f"Handle exemption for all zones"

    async def async_update(self):
        self._attr_state = ButtonState.ENABLED if self._zone.detail.is_exemption_enabled else ButtonState.DISABLED
        self._attr_native_value = ExemptionButtonState[self._attr_state].value
