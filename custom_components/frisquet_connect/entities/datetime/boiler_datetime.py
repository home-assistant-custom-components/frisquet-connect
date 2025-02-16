from homeassistant.components.datetime import DateTimeEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import (
    DATETIME_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity


class BoilerDateTime(DateTimeEntity, CoordinatorEntity, CoreEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)

        self._attr_unique_id = (
            f"{self.coordinator_typed.site.site_id}_{DATETIME_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY}"
        )
        self._attr_translation_key = DATETIME_CURRENT_BOILER_DATETIME_TRANSLATIONS_KEY

    async def async_update(self):
        self._attr_native_value = self.coordinator_typed.site.detail.current_boiler_timestamp
