import logging
from homeassistant.helpers.entity import Entity
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import FrisquetConnectCoordinator
from custom_components.frisquet_connect.entities.utils import get_device_info


_LOGGER = logging.getLogger(__name__)


class CoreEntity(Entity):
    """Base class for all entities."""

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    @property
    def device_info(self):
        return get_device_info(self.name, self.unique_id, self.coordinator_typed)

    @property
    def should_poll(self) -> bool:
        return True
