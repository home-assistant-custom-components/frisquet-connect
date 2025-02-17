import logging
from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import ConsumptionType
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity
from custom_components.frisquet_connect.utils import log_methods


_LOGGER = logging.getLogger(__name__)


@log_methods
class CoreConsumption(SensorEntity, CoordinatorEntity, CoreEntity):

    _consumption_type: ConsumptionType

    def __init__(self, coordinator: FrisquetConnectCoordinator, translation_key: str) -> None:
        super().__init__(coordinator)
        CoreEntity.__init__(self)

        self._attr_unique_id = f"{self.coordinator_typed.site.site_id}_{translation_key}"
        self._attr_translation_key = translation_key

        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_unit_of_measurement = "kWh"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    async def async_update(self):
        if not self._consumption_type:
            _LOGGER.error("Consumption type not set")
            return

        current_year = datetime.now().year
        native_value = 0
        consumptions = self.coordinator_typed.site.get_consumptions_by_type(self._consumption_type)
        if consumptions:
            for consumption_month in consumptions.consumption_months:
                if consumption_month.year == current_year:
                    native_value += consumption_month.value
        self._attr_native_value = native_value
