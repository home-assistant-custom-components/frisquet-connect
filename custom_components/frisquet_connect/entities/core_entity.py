import logging
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.core import callback

from custom_components.frisquet_connect.const import DEVICE_MANUFACTURER, DOMAIN
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import FrisquetConnectCoordinator
from custom_components.frisquet_connect.utils import log_methods


_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/integration_fetching_data?_highlight=scan_interval#separate-polling-for-each-individual-entity
# https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/appropriate-polling?_highlight=_attr_should_poll#example-implementation
@log_methods
class CoreEntity(CoordinatorEntity[FrisquetConnectCoordinator]):
    """Base class for all entities."""

    def __init__(self, coordinator: FrisquetConnectCoordinator) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating CoreEntity '{self.__class__.__name__}'")

        self._attr_has_entity_name = True
        self._attr_should_poll = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data.site_id)},
            name=self.coordinator.data.name,
            manufacturer=DEVICE_MANUFACTURER,
            model=str(self.coordinator.data.product),
            serial_number=self.coordinator.data.serial_number,
        )

    @callback
    async def _handle_coordinator_update(self) -> None:
        await self.async_update()
