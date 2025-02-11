import logging
from typing import Tuple

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import (
    FrisquetConnectService,
)


_LOGGER = logging.getLogger(__name__)


async def async_initialize_entity(
    hass: HomeAssistant, entry: ConfigEntry, entity_name: str
) -> Tuple[bool, FrisquetConnectCoordinator]:
    _LOGGER.debug(f"Initializing entity '{entity_name}'")

    initialization_result = True
    coordinator: FrisquetConnectCoordinator = None

    if entry.data.get("site_id") is None:
        _LOGGER.error("No site_id found in the config entry. Please configure the device")
        initialization_result = False
    else:
        service: FrisquetConnectService = hass.data[DOMAIN][entry.unique_id]
        coordinator = FrisquetConnectCoordinator(hass, service, entry.data["site_id"])
        await coordinator._async_update()

        if not coordinator.is_site_loaded:
            _LOGGER.error("Site not found")
            initialization_result = False

    _LOGGER.debug(f"Initialization result for entity '{entity_name}' : {initialization_result}")

    return (initialization_result, coordinator)
