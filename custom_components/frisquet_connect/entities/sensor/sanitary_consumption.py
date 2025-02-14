from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.const import (
    SENSOR_SANITARY_CONSUMPTION_TRANSLATIONS_KEY,
)
from custom_components.frisquet_connect.entities.sensor.core_consumption import (
    CoreConsumption,
)


class SanitaryConsumptionEntity(CoreConsumption):

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator, SENSOR_SANITARY_CONSUMPTION_TRANSLATIONS_KEY)
