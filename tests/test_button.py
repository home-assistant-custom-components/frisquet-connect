from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect.button import async_setup_entry
from custom_components.frisquet_connect.const import DOMAIN
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.devices.frisquet_connect_device import (
    FrisquetConnectDevice,
)
from custom_components.frisquet_connect.entities.button.refresh_data import (
    RefreshDataButton,
)
from tests.utils import mock_endpoints, unstub_all


@pytest.mark.asyncio
async def test_refresh_button(
    mock_hass: HomeAssistant,
    mock_entry: ConfigEntry,
    mock_add_entities: AddEntitiesCallback,
) -> None:
    mock_endpoints()

    service = FrisquetConnectDevice(
        mock_entry.data.get("email"),
        mock_entry.data.get("password"),
    )
    coordinator = FrisquetConnectCoordinator(
        mock_hass,
        service,
        mock_entry.data.get("site_id"),
    )
    await coordinator._async_refresh()
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: coordinator}

    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]
    assert len(entities) == 1
    assert isinstance(entities[0], RefreshDataButton)

    with patch.object(coordinator, "async_refresh", new=AsyncMock()) as async_refresh:
        await entities[0].async_press()
        async_refresh.assert_awaited_once_with()

    unstub_all()
