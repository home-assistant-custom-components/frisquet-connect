import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect_unofficial.const import HEATING_CONSUMPTION_TRANSLATIONS_KEY
from custom_components.frisquet_connect_unofficial.entities.sensor.core_consumption import (
    CoreConsumption,
)


LOGGER = logging.getLogger(__name__)


class HeatingConsumptionEntity(CoreConsumption):

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator, HEATING_CONSUMPTION_TRANSLATIONS_KEY)
