import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class CoreConsumption(SensorEntity, CoordinatorEntity):
    _site: Site

    def __init__(self, coordinator: FrisquetConnectCoordinator, suffix_id: str, label: str) -> None:
        super().__init__(coordinator)

        self._site = coordinator.site
        self._attr_unique_id = f"{self._site.site_id}_{suffix_id}"
        self._attr_name = label
        self._attr_has_entity_name = True

        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_unit_of_measurement = "kWh"

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
