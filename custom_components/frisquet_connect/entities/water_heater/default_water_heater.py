from homeassistant.components.water_heater import WaterHeaterEntity, WaterHeaterEntityFeature

from custom_components.frisquet_connect.const import WATER_HEATER_TRANSLATIONS_KEY, SanitaryWaterModeLabel
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity
from homeassistant.core import callback


class DefaultWaterHeaterEntity(CoreEntity, WaterHeaterEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}_{WATER_HEATER_TRANSLATIONS_KEY}"
        self._attr_has_entity_name = True
        self._attr_translation_key = WATER_HEATER_TRANSLATIONS_KEY

        self._attr_supported_features = WaterHeaterEntityFeature.OPERATION_MODE
        self._attr_temperature_unit = "°C"
        self._attr_operation_list = coordinator.site.available_sanitary_water_modes

    @callback
    def _handle_coordinator_update(self) -> None:
        self.current_operation = SanitaryWaterModeLabel[
            self.coordinator_typed.site.water_heater.sanitary_water_mode.name
        ]

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        await self.coordinator_typed.service.async_set_sanitary_water_mode(
            self.coordinator_typed.site.site_id, operation_mode
        )
