from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.frisquet_connect_unofficial.domains.exceptions.forbidden_access_exception import (
    ForbiddenAccessException,
)
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.devices.frisquet_connect_device import (
    FrisquetConnectDevice,
)


_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=300)


class FrisquetConnectCoordinator(DataUpdateCoordinator):
    _service: FrisquetConnectDevice
    _site_id: str
    _site: Site

    def __init__(self, hass: HomeAssistant, service: FrisquetConnectDevice, site_id: str):
        super().__init__(
            hass,
            _LOGGER,
            name="Frisquet Connect Coordinator",
            update_interval=SCAN_INTERVAL,
            update_method=self._async_update,
        )
        self._service = service
        self._site_id = site_id
        self._site = None

    async def _async_update(self):
        try_count = 1
        while try_count >= 0:
            _LOGGER.debug(f"Fetching data for site {self._site_id} (try {try_count})")
            try_count -= 1
            try:
                self._site = await self._service.async_get_site_info(self._site_id)
                break
            except ForbiddenAccessException:
                await self._service.async_refresh_token_and_sites()
            except Exception as e:
                _LOGGER.error(f"Error unknown during fetching data: {e}")

    @property
    def is_site_loaded(self) -> bool:
        return self._site is not None

    @property
    def site(self) -> Site:
        return self._site

    @property
    def service(self) -> FrisquetConnectDevice:
        return self._service
