from custom_components.entities.sensor.core_thermometer import CoreThermometer
from custom_components.frisquet_connect.const import OUTSIDE_THERMOMETER_LABEL
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator


class InsideThermoeterEntity(CoreThermometer):
    _zone: Zone

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator, f"outside-{zone_label_id}", f"{OUTSIDE_THERMOMETER_LABEL}_{zone_label_id}")
        self._zone = self._site.get_zone_by_label_id(zone_label_id)

    async def async_update(self):
        self._attr_native_value = self._zone.detail.current_temperature
