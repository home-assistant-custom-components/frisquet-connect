from homeassistant.components.water_heater import WaterHeaterEntity, WaterHeaterEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.domains.site.water_heater import WaterHeater
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


class DefaultWaterHeaterEntity(WaterHeaterEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)

        self._attr_unique_id = f"water_heater_{coordinator.site.site_id}"
        self._attr_name = f"Water Heater at {coordinator.site.name}"
        self._attr_has_entity_name = True

        self._attr_supported_features = WaterHeaterEntityFeature.OPERATION_MODE
        self._attr_temperature_unit = "°C"
        self._attr_operation_list = coordinator.site.available_sanitary_water_modes

    @property
    def should_poll(self) -> bool:
        return True

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        coordinator: FrisquetConnectCoordinator = self.coordinator
        coordinator.service.set_sanitary_water_mode(self._site, operation_mode)

    async def async_update(self):
        self.current_operation = self._site.water_heater.sanitary_water_mode
