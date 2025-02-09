import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.components.climate import DOMAIN
from custom_components.frisquet_connect_unofficial.domains.exceptions.forbidden_access_exception import (
    ForbiddenAccessException,
)
from custom_components.frisquet_connect_unofficial.domains.site.site_light import SiteLight
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import (
    FrisquetConnectService,
)

from .const import DOMAIN


LOGGER = logging.getLogger(__name__)


class FrisquetConnectFlow(ConfigFlow, domain=DOMAIN):

    VERSION = 1
    _user_input: dict = dict()
    _errors: dict[str, str] | None = None

    def _get_vol_schema_for_authentication(self):
        return vol.Schema({vol.Required("email"): str, vol.Required("password"): str})

    def _get_vol_schema_for_site(self):
        return vol.Schema({vol.Required("site", default=0): vol.In(self._user_input["sites"])})

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        # Ask for credentials if not already done
        if user_input is None:
            LOGGER.error("Asking for authentication")
            return self.async_show_form(step_id="credentials", data_schema=self._get_vol_schema_for_authentication())

        # Then update user_input
        self._user_input.update(user_input)

        # Finally, go to the next step
        return await self._set_auhentication_step()

    async def _set_auhentication_step(self) -> FlowResult:
        # Get existing sites if not already done
        if self._user_input.get("sites") is None:
            service = FrisquetConnectService(self._user_input.get("email"), self._user_input.get("password"))
            try:
                authentication = await service.async_refresh_token_and_sites()
                self._user_input["sites"] = authentication.sites
            except ForbiddenAccessException:
                errors = {"base": "invalid_credentials"}
                return self.async_show_form(
                    step_id="credentials", data_schema=self._get_vol_schema_for_authentication(), errors=errors
                )
            except Exception as e:
                return self.async_abort(reason=e.message)

        # Finally, go to the next step
        return await self._set_site_step()

    async def _set_site_step(self) -> FlowResult:
        # No site so not possible to go further
        if len(self._user_input["sites"]) == 0:
            LOGGER.error("No site found")
            return self.async_abort(reason="No site found")

        # Ask for site if not already done
        elif self._user_input.get("site") is None:
            LOGGER.info("Asking for site")
            return self.async_show_form(step_id="site_id", data_schema=self._get_vol_schema_for_site())

        site_light: SiteLight = self._user_input["sites"].index(self._user_input["site"])
        await self.async_set_unique_id(site_light.site_id)
        return self.async_create_entry(title=site_light.name, data=site_light)
