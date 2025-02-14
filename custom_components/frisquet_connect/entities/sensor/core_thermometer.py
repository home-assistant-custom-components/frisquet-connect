import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.utils import get_device_info
from custom_components.frisquet_connect.utils import log_methods

_LOGGER = logging.getLogger(__name__)


@log_methods
class CoreThermometer(SensorEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator, translation_key: str, suffix: str = None) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating CoreThermometer entity for {translation_key}")

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}_{translation_key}{suffix}"
        self._attr_has_entity_name = True
        self._attr_translation_key = translation_key

        self._attr_native_unit_of_measurement = "°C"
        self._attr_unit_of_measurement = "°C"

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.name, self.unique_id, self.coordinator)

    @property
    def icon(self) -> str | None:
        return "mdi:thermometer"

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.TEMPERATURE

    @property
    def state_class(self) -> SensorStateClass | None:
        return SensorStateClass.MEASUREMENT
