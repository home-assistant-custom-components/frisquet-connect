import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import SANITARY_CONSUMPTION_LABEL
from custom_components.frisquet_connect.entities.sensor.core_consumption import CoreConsumption


LOGGER = logging.getLogger(__name__)


class SanitaryConsumptionEntity(CoreConsumption):

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator, "sanitary", SANITARY_CONSUMPTION_LABEL)
