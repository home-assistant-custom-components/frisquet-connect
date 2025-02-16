from custom_components.frisquet_connect.const import (
    SENSOR_INSIDE_THERMOMETER_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.entities.core_entity import CoreEntity
from custom_components.frisquet_connect.entities.sensor.core_thermometer import (
    CoreThermometer,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


class InsideThermometerEntity(CoreThermometer):
    _zone_label_id: str

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, SENSOR_INSIDE_THERMOMETER_TRANSLATIONS_KEY, zone_label_id)
        CoreEntity.__init__(self)

        self._zone_label_id = zone_label_id
        self._attr_translation_placeholders = {"zone_name": self.zone.name}

    @property
    def zone(self) -> Zone:
        return self.coordinator_typed.site.get_zone_by_label_id(self._zone_label_id)

    async def async_update(self):
        self._attr_native_value = self.zone.detail.current_temperature
