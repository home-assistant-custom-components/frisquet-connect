import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.utils import get_device_info
from custom_components.frisquet_connect.utils import log_methods


_LOGGER = logging.getLogger(__name__)


@log_methods
class CoreConsumption(SensorEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator, translation_key: str) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating CoreConsumption entity for {translation_key}")

        self._attr_unique_id = f"{self.coordinator.site.site_id}_{translation_key}"
        self._attr_has_entity_name = True
        self._attr_translation_key = translation_key
        self._attr_translation_placeholders = {"site_name": coordinator.site.name}

        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_unit_of_measurement = "kWh"

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.name, self.unique_id, self.coordinator)

    @property
    def icon(self) -> str | None:
        return "mdi:gas-burner"

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.ENERGY

    @property
    def state_class(self) -> SensorStateClass | None:
        return SensorStateClass.TOTAL

    async def async_update(self):
        # self._attr_native_value = self._site.consumptions["sanitary"]
        # TODO: Implement this
        pass
