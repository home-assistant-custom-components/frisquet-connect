import logging
from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect.const import DEVICE_MANUFACTURER, DEVICE_NAME, DOMAIN
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from homeassistant.helpers.entity import Entity
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import FrisquetConnectCoordinator


_LOGGER = logging.getLogger(__name__)


class CoreEntity(Entity):
    """Base class for all entities."""

    def __init__(self):
        super().__init__()
        _LOGGER.debug(f"Creating CoreEntity '{self.__class__.__name__}'")

        self._attr_has_entity_name = True

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=f"{DEVICE_NAME} ({self.coordinator_typed.site.name})",
            manufacturer=DEVICE_MANUFACTURER,
            model=self.coordinator_typed.site.product,
            serial_number=self.coordinator_typed.site.serial_number,
            via_device=(DOMAIN, self.coordinator_typed.site.site_id),
        )

    @property
    def should_poll(self) -> bool:
        return True
