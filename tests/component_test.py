import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from custom_components.frisquet_connect_unofficial import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN, PLATFORMS
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from tests.utils import read_json_file


async def async_magic():
    pass


MagicMock.__await__ = lambda x: async_magic().__await__()
AsyncMock.__await__ = lambda x: async_magic().__await__()


@pytest.fixture
def mock_hass():
    mock = AsyncMock(spec=HomeAssistant)
    mock.data = {}
    return mock


@pytest.fixture
def mock_entry():
    mock_entry_file = read_json_file("mock_entry.json")
    mock = AsyncMock(spec=ConfigEntry)
    mock.data = mock_entry_file.get("data")
    mock.unique_id = mock_entry_file.get("unique_id")
    return mock


@pytest.mark.asyncio
async def test_async_setup_entry_success(mock_hass: HomeAssistant, mock_entry: ConfigEntry):
    with patch.object(
        mock_hass.config_entries, "async_forward_entry_setups", return_value=AsyncMock()
    ) as mock_forward:
        result = await async_setup_entry(mock_hass, mock_entry)

        assert result is True
        assert mock_hass.data[DOMAIN][mock_entry.unique_id] is not None
        assert isinstance(mock_hass.data[DOMAIN][mock_entry.unique_id], FrisquetConnectService)
        mock_forward.assert_called_once_with(mock_entry, PLATFORMS)


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(mock_hass, mock_entry):
    mock_entry.data = {"site_id ": None}

    result = await async_setup_entry(mock_hass, mock_entry)

    assert result is False
    assert DOMAIN not in mock_hass.data
