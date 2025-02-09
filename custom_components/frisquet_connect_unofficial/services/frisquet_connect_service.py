import logging

from custom_components.frisquet_connect_unofficial.const import SanitaryWaterMode, ZoneSelector
from custom_components.frisquet_connect_unofficial.domains.authentication.authentication import (
    Authentication,
)
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.domains.site.site_light import SiteLight
from custom_components.frisquet_connect_unofficial.domains.site.utils import (
    convert_hass_temperature_to_int,
)
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.repositories.frisquet_connect_repository import (
    FrisquetConnectRepository,
)


LOGGER = logging.getLogger(__name__)


class FrisquetConnectService:
    _repository: FrisquetConnectRepository
    _email: str
    _password: str
    _sites: list[SiteLight]
    _token: str

    def __init__(self, email: str, password: str) -> None:
        self._email = email
        self._password = password
        self._repository = FrisquetConnectRepository()
        self._sites = []
        self._token = ""

    async def async_refresh_token_and_sites(self) -> Authentication:
        authentication = await self._repository.async_get_token_and_sites(self._email, self._password)
        self._token = authentication.token
        self._sites = authentication.sites
        return authentication

    @property
    def sites(self) -> list[SiteLight]:
        return self._sites

    async def async_get_site_info(self, site_id: str) -> Site:
        return await self._repository.async_get_site_info(site_id, self._token)

    async def async_set_temperature(self, site_id: str, zone: Zone, temperature: float) -> None:
        api_temperature = convert_hass_temperature_to_int(temperature)
        await self._repository.async_set_temperature(
            site_id, zone.label_id, zone.detail.mode, api_temperature, self._token
        )

    async def async_set_selector(self, site_id: str, zone: Zone, selector: ZoneSelector) -> None:
        await self._repository.async_set_selector(site_id, zone.label_id, selector, self._token)

    async def async_set_sanitary_water_mode(self, site_id: str, mode: str) -> None:
        mapped_mode = SanitaryWaterMode(mode)
        await self._repository.async_set_sanitary_water_mode(site_id, mapped_mode, self._token)

    ###

    async def async_set_exemption(self, site_id: str, selector: ZoneSelector) -> None:
        await self._repository.async_set_exemption(site_id, selector, self._token)

    async def async_cancel_exemption(self, site_id: str) -> None:
        await self._repository.async_set_exemption(site_id, ZoneSelector.AUTO, self._token)

    async def async_enable_boost(self, site_id: str, zone: Zone) -> None:
        await self._repository.async_set_boost(site_id, zone.label_id, True, self._token)

    async def async_disable_boost(self, site_id: str, zone: Zone) -> None:
        await self._repository.async_set_boost(site_id, zone.label_id, False, self._token)
