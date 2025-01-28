from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.frisquet_connect_unofficial.domains.exceptions.forbidden_access_exception import (
    ForbiddenAccessException,
)
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService


LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=300)


class FrisquetConnectCoordinator(DataUpdateCoordinator):
    _service: FrisquetConnectService
    _site_id: str
    _site: Site

    def __init__(self, hass: HomeAssistant, service: FrisquetConnectService, site_id: str):
        super().__init__(
            hass,
            LOGGER,
            name="Frisquet Connect Coordinator",
            update_interval=SCAN_INTERVAL,
        )
        self._service = service
        self._site_id = site_id

    async def _async_update_data(self):
        try_count = 1
        while try_count >= 0:
            try_count -= 1
            try:
                self._site = await self._service.get_site_info(self._site_id)
            except ForbiddenAccessException:
                await self._service.refresh_token_and_sites()
            except Exception as e:
                LOGGER.error(f"Error unknown during fetching data: {e}")

    @property
    def site(self) -> Site:
        return self._site

    @property
    def service(self) -> FrisquetConnectService:
        return self._service
