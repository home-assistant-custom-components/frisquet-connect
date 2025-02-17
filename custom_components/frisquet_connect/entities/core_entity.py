import logging
from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect.const import DEVICE_MANUFACTURER, DOMAIN
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from homeassistant.helpers.entity import Entity
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import FrisquetConnectCoordinator
from custom_components.frisquet_connect.utils import log_methods


_LOGGER = logging.getLogger(__name__)


@log_methods
class CoreEntity(Entity):
    """Base class for all entities."""

    def __init__(self):
        super().__init__()
        _LOGGER.debug(f"Creating CoreEntity '{self.__class__.__name__}'")

        self._attr_has_entity_name = True
        self._attr_should_poll = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator_typed.site.site_id)},
            name=self.coordinator_typed.site.name,
            manufacturer=DEVICE_MANUFACTURER,
            model=str(self.coordinator_typed.site.product),
            serial_number=self.coordinator_typed.site.serial_number,
        )

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator
