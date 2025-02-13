import logging
from homeassistant.components.water_heater import WaterHeaterEntity, WaterHeaterEntityFeature
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect_unofficial.const import WATER_HEATER_TRANSLATIONS_KEY, SanitaryWaterModeLabel
from custom_components.frisquet_connect_unofficial.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect_unofficial.entities.utils import get_device_info

_LOGGER = logging.getLogger(__name__)


class DefaultWaterHeaterEntity(WaterHeaterEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating WaterHeater entity")

        self._attr_unique_id = f"water_heater_{coordinator.site.site_id}"
        self._attr_has_entity_name = True
        self._attr_translation_key = WATER_HEATER_TRANSLATIONS_KEY
        self._attr_translation_placeholders = {"site_name": coordinator.site.name}

        self._attr_supported_features = WaterHeaterEntityFeature.OPERATION_MODE
        self._attr_temperature_unit = "°C"
        self._attr_operation_list = coordinator.site.available_sanitary_water_modes

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.name, self.unique_id, self.coordinator)

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await self.async_update()

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        self.coordinator_typed.service.async_set_sanitary_water_mode(
            self.coordinator_typed.site.site_id, operation_mode
        )

    async def async_update(self):
        self.current_operation = SanitaryWaterModeLabel[self.coordinator_typed.site.water_heater.sanitary_water_mode]
