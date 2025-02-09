import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.frisquet_connect_unofficial.config_flow import FrisquetConnectFlow
from tests.utils import unstub_all


@pytest.mark.asyncio
async def test_async_config_flow(mock_hass: HomeAssistant, mock_entry: ConfigEntry):
    config_flow = FrisquetConnectFlow()

    user_input = None
    await config_flow.async_step_user(user_input)

    user_input = {"email": "firstname.lastname@domain.com", "password": "p@ssw0rd"}
    await config_flow.async_step_user(user_input)

    unstub_all()
