from custom_components.frisquet_connect_unofficial.const import (
    OUTSIDE_THERMOMETER_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect_unofficial.entities.sensor.core_thermometer import (
    CoreThermometer,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


class OutsideThermoeterEntity(CoreThermometer):

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator, "outside", OUTSIDE_THERMOMETER_TRANSLATIONS_KEY)
        self._attr_translation_placeholders = {"site_name": coordinator.site.name}

    async def async_update(self):
        self._attr_native_value = self._site.external_temperature
