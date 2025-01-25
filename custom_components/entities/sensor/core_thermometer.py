from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import DOMAIN
from custom_components.frisquet_connect.domains.site.site import Site
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator


class CoreThermometer(SensorEntity, CoordinatorEntity):
    _site: Site

    def __init__(self, coordinator: FrisquetConnectCoordinator, suffix_id: str, label: str) -> None:
        super().__init__(coordinator)

        self._site = coordinator.site
        self._attr_unique_id = f"{self._site.site_id}_{suffix_id}"
        self._attr_name = label
        self._attr_has_entity_name = True

        self._attr_native_unit_of_measurement = "°C"
        self._attr_unit_of_measurement = "°C"

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
