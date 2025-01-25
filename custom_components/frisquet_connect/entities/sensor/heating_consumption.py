import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.entities.sensor.core_consumption import CoreConsumption
from custom_components.frisquet_connect.const import HEATING_CONSUMPTION_LABEL


LOGGER = logging.getLogger(__name__)


class HeatingConsumptionEntity(CoreConsumption):

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator, "heating", HEATING_CONSUMPTION_LABEL)
