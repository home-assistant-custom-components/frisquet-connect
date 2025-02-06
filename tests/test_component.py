import pytest
from unittest.mock import AsyncMock, patch
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.frisquet_connect_unofficial import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN, PLATFORMS
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from tests.conftest import async_core_setup_entry_no_site_id
from tests.utils import mock_endpoints, unstub_all


@pytest.mark.asyncio
async def test_async_setup_entry_success(mock_hass: HomeAssistant, mock_entry: ConfigEntry):
    # Initialize the mocks
    mock_endpoints()

    # Test the feature
    with patch.object(
        mock_hass.config_entries, "async_forward_entry_setups", return_value=AsyncMock()
    ) as mock_forward:
        result = await async_setup_entry(mock_hass, mock_entry)

        # Assertions
        assert result is True
        assert mock_hass.data[DOMAIN][mock_entry.unique_id] is not None
        assert isinstance(mock_hass.data[DOMAIN][mock_entry.unique_id], FrisquetConnectService)
        mock_forward.assert_called_once_with(mock_entry, PLATFORMS)


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(mock_hass: HomeAssistant, mock_entry: ConfigEntry):
    await async_core_setup_entry_no_site_id(async_setup_entry, None, mock_hass, mock_entry)
    unstub_all()
