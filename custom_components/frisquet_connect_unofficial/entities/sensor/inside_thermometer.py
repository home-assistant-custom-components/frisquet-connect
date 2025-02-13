from custom_components.frisquet_connect_unofficial.const import (
    SENSOR_INSIDE_THERMOMETER_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.sensor.core_thermometer import (
    CoreThermometer,
)
from custom_components.frisquet_connect_unofficial.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


class InsideThermoeterEntity(CoreThermometer):
    _zone: Zone

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(
            coordinator,
            f"inside-{zone_label_id}",
            f"{SENSOR_INSIDE_THERMOMETER_TRANSLATIONS_KEY}_{zone_label_id}",
        )

        self._zone = self._site.get_zone_by_label_id(zone_label_id)
        self._attr_translation_placeholders = {"zone_name": self._zone.name}

    async def async_update(self):
        self._attr_native_value = self._zone.detail.current_temperature
