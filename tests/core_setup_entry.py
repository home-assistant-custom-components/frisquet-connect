from typing import Any, Coroutine

import homeassistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService


async def async_core_setup_entry_no_site_id(
    async_setup_entry: Coroutine[Any, Any, None],
    mock_hass: homeassistant,
    mock_entry: ConfigEntry,
    mock_add_entities: AddEntitiesCallback = None,
):
    mock_entry.data = {"site_id ": None}

    service = FrisquetConnectService(mock_entry)
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: service}
    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    if mock_add_entities:
        mock_add_entities.assert_called_once()
        entities = mock_add_entities.call_args[0][0]
        assert len(entities) == 0
