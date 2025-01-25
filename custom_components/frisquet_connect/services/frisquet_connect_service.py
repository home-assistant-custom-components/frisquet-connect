import logging
from homeassistant.config_entries import ConfigEntry

from custom_components.frisquet_connect.const import PRESET_MODE_ORDERS_MAPPING, ZoneSelector
from custom_components.frisquet_connect.domains.authentication.authentication import Authentication
from custom_components.frisquet_connect.domains.site.site import Site
from custom_components.frisquet_connect.domains.site.site_light import SiteLight
from custom_components.frisquet_connect.domains.site.utils import convert_hass_temperature_to_int
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.repositories.frisquet_connect_repository import FrisquetConnectRepository


LOGGER = logging.getLogger(__name__)


class FrisquetConnectService:
    _repository: FrisquetConnectRepository
    _entry: ConfigEntry
    _sites: list[SiteLight]
    _token: str

    def __init__(self, entry: ConfigEntry):
        self._entry = entry
        self._repository = FrisquetConnectRepository()

    def _get_email(self) -> str:
        return self._entry.data["email"]

    def _get_password(self) -> str:
        return self._entry.data["password"]

    async def refresh_token_and_sites(self) -> Authentication:
        authentication = self._repository.get_token_and_sites(self._get_email(), self._get_password())
        self._token = authentication.token
        self._sites = authentication.sites
        return authentication

    @property
    def sites(self) -> list[SiteLight]:
        return self._sites

    async def get_site_info(self, site_id: str) -> Site:
        return await self._repository.get_site_info(site_id, self._token)

    async def set_temperature(self, site_id: str, zone: Zone, temperature: float) -> None:
        api_temperature = convert_hass_temperature_to_int(temperature)
        await self._repository.set_temperature(site_id, zone.label_id, zone.detail.mode, api_temperature, self._token)

    async def set_selector(self, site_id: str, zone: Zone, selector: ZoneSelector) -> None:
        await self._repository.set_selector(site_id, zone.label_id, selector, self._token)

    ###

    async def set_exemption(self, site_id: str, selector: ZoneSelector) -> None:
        await self._repository.set_exemption(site_id, selector, self._token)

    async def cancel_exemption(self, site_id: str) -> None:
        await self._repository.set_exemption(site_id, ZoneSelector.AUTO, self._token)

    async def enable_boost(self, site_id: str, zone: Zone) -> None:
        await self._repository.set_boost(site_id, zone.label_id, True, self._token)

    async def disable_boost(self, site_id: str, zone: Zone) -> None:
        await self._repository.set_boost(site_id, zone.label_id, False, self._token)
