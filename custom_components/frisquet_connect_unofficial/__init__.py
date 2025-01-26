"""Initialisation du package de l'intégration Frisquet Connect"""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from .const import (
    DOMAIN,
    PLATFORMS,
)


LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    LOGGER.debug("Initializating Frisquet Connect")

    site_id = entry.data.get("site_id")
    if site_id is None:
        LOGGER.error("No site_id found - Please reconfigure the integration")
        return False

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.unique_id] = FrisquetConnectService(entry.data)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
