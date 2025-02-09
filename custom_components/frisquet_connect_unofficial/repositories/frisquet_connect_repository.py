import logging

from custom_components.frisquet_connect_unofficial.const import (
    BOOST_ORDER_LABEL,
    EXEMPTION_ORDER_LABEL,
    SANITARY_WATER_ORDER_LABEL,
    SELECTOR_ORDER_LABEL,
    SanitaryWaterMode,
    ZoneMode,
    ZoneModeLabelOrder,
    ZoneSelector,
)
from custom_components.frisquet_connect_unofficial.domains.authentication.authentication_request import (
    AuthenticationRequest,
)
from custom_components.frisquet_connect_unofficial.domains.authentication.authentication import (
    Authentication,
)
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.repositories.core_repository import (
    async_do_get,
    async_do_post,
)


FRISQUET_CONNECT_URL = "https://fcutappli.frisquet.com/api/v1"

AUTH_ENDPOINT = f"{FRISQUET_CONNECT_URL}/authentifications"

SITES_ENDPOINT = f"{FRISQUET_CONNECT_URL}/sites"
SITES_CONSO_ENDPOINT = "{SITES_ENDPOINT}/conso"

ORDER_ENDPOINT = f"{FRISQUET_CONNECT_URL}/ordres"


LOGGER = logging.getLogger(__name__)


class FrisquetConnectRepository:

    async def async_get_token_and_sites(self, email: str, password: str) -> Authentication:
        LOGGER.debug("Getting token and existing sites")

        payload = AuthenticationRequest(email, password).to_dict()
        response_json = await async_do_post(AUTH_ENDPOINT, None, payload)
        return Authentication(response_json)

    async def async_get_site_info(self, site_id: str, token: str) -> Site:
        LOGGER.debug("Getting site info")

        params = {"token": token}
        response_json = await async_do_get(f"{SITES_ENDPOINT}/{site_id}", params)
        return Site(response_json)

    async def async_get_site_conso(self, site_id: str, token: str) -> dict:
        LOGGER.debug("Getting site conso")

        params = {"token": token, "types": ["CHF", "SAN"]}
        response_json = await async_do_get(SITES_CONSO_ENDPOINT.format(site_id=site_id), params)
        return response_json  # TODO do an object for this

    async def async_set_temperature(
        self, site_id: str, zone_id: str, zone_mode: ZoneMode, temperature: int, token: str
    ) -> dict:
        LOGGER.debug("Setting temperature")

        mode_target = ZoneModeLabelOrder[zone_mode.name].value
        key = f"{mode_target}_{zone_id}"

        payload = [{"cle": key, "valeur": temperature}]
        response_json = await self._async_do_site_action(site_id, token, payload)
        return response_json

    async def async_set_sanitary_water_mode(
        self, site_id: str, sanitary_water_mode: SanitaryWaterMode, token: str
    ) -> dict:
        LOGGER.debug("Setting sanitary water mode")

        payload = [{"cle": SANITARY_WATER_ORDER_LABEL, "valeur": sanitary_water_mode.value}]
        response_json = await self._async_do_site_action(site_id, token, payload)
        return response_json

    async def async_set_selector(
        self, site_id: str, zone_id: str, zone_selector: ZoneSelector, token: str
    ) -> dict:
        LOGGER.debug("Setting selector")

        key = f"{SELECTOR_ORDER_LABEL}_{zone_id}"
        selector_target = ZoneSelector[zone_selector.name].value

        payload = [{"cle": key, "valeur": selector_target}]
        response_json = await self._async_do_site_action(site_id, token, payload)
        return response_json

    async def async_set_exemption(
        self, site_id: str, zone_selector: ZoneSelector, token: str
    ) -> dict:
        LOGGER.debug("Setting exemption")

        # TODO : Check if the preset_mode is AUTO
        if zone_selector not in [
            ZoneSelector.AUTO,
            ZoneSelector.COMFORT_PERMANENT,
            ZoneSelector.REDUCED_PERMANENT,
        ]:
            error_message = f"Incompatible zone selector: {zone_selector}"
            LOGGER.error(error_message)
            raise ValueError(error_message)

        value = 0 if zone_selector == ZoneSelector.AUTO else zone_selector.value

        payload = [{"cle": EXEMPTION_ORDER_LABEL, "valeur": value}]
        response_json = await self._async_do_site_action(site_id, token, payload)
        return response_json

    async def async_set_boost(self, site_id: str, zone_id: str, enable: bool, token: str) -> dict:
        LOGGER.debug("Setting exemption")

        key = f"{BOOST_ORDER_LABEL}_{zone_id}"
        value = 1 if enable else 0

        payload = [{"cle": key, "valeur": value}]
        response_json = await self._async_do_site_action(site_id, token, payload)
        return response_json

    async def _async_do_site_action(self, site_id: str, token: str, payload: list[dict]) -> dict:
        LOGGER.debug("Doing site action")

        params = {"token": token}
        response_json = await async_do_post(f"{ORDER_ENDPOINT}/{site_id}", params, payload)
        return response_json
