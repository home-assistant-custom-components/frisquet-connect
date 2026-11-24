from homeassistant.components.button import ButtonEntity

from custom_components.frisquet_connect.const import (
    BUTTON_REFRESH_DATA_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity


class RefreshDataButton(CoreEntity, ButtonEntity):
    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)

        self._attr_unique_id = f"{coordinator.data.site_id}_{BUTTON_REFRESH_DATA_TRANSLATIONS_KEY}"
        self._attr_translation_key = BUTTON_REFRESH_DATA_TRANSLATIONS_KEY

    def update(self) -> None:
        pass

    async def async_press(self) -> None:
        await self.coordinator.async_refresh()
