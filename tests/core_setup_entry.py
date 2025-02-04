from typing import Any, Coroutine

from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from tests.utils import mock_endpoints, mock_entry, mock_hass


async def async_core_setup_entry_no_site_id(
    async_setup_entry: Coroutine[Any, Any, None],
    mock_add_entities: AddEntitiesCallback = None,
):
    # Initialize the mocks
    mock_endpoints()
    hass = mock_hass()
    hass.data = {"site_id ": None}
    entry = mock_entry()

    service = FrisquetConnectService(entry)
    hass.data[DOMAIN] = {entry.unique_id: service}
    await async_setup_entry(hass, entry, mock_add_entities)

    if mock_add_entities:
        mock_add_entities.assert_called_once()
        entities = mock_add_entities.call_args[0][0]
        assert len(entities) == 0
