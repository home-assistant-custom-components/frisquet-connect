import pytest
from unittest.mock import AsyncMock, patch
from custom_components.frisquet_connect_unofficial import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN, PLATFORMS
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from tests.core_setup_entry import async_core_setup_entry_no_site_id
from tests.utils import mock_endpoints, mock_hass, mock_entry, unstub_all


@pytest.mark.asyncio
async def test_async_setup_entry_success():
    # Initialize the mocks
    mock_endpoints()
    hass = mock_hass()
    entry = mock_entry()

    # Test the feature
    with patch.object(hass.config_entries, "async_forward_entry_setups", return_value=AsyncMock()) as mock_forward:
        result = await async_setup_entry(hass, entry)

        # Assertions
        assert result is True
        assert hass.data[DOMAIN][entry.unique_id] is not None
        assert isinstance(hass.data[DOMAIN][entry.unique_id], FrisquetConnectService)
        mock_forward.assert_called_once_with(entry, PLATFORMS)


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id():
    async_core_setup_entry_no_site_id(async_setup_entry)
    unstub_all()