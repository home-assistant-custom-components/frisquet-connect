from datetime import datetime
import os
import pytest
from unittest.mock import AsyncMock
from tests.utils import mock_endpoints, mock_hass, mock_entry

from unittest.mock import AsyncMock
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect_unofficial.climate import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.climate.default_climate import DefaultClimateEntity
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from tests.core_setup_entry import async_core_setup_entry_no_site_id


@pytest.fixture
def mock_add_entities():
    return AsyncMock(spec=AddEntitiesCallback)


@pytest.mark.asyncio
async def test_async_setup_entry_success(mock_add_entities: AddEntitiesCallback):
    # Initialize the mocks
    mock_endpoints()
    hass = mock_hass()
    entry = mock_entry()

    # Test the feature
    service = FrisquetConnectService(entry)
    hass.data[DOMAIN] = {entry.unique_id: service}
    await async_setup_entry(hass, entry, mock_add_entities)

    # Assertions
    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]

    assert len(entities) == 1
    assert isinstance(entities[0], DefaultClimateEntity)

    entity: DefaultClimateEntity = entities[0]
    zone: Zone = entity._zone
    assert zone is not None
    assert entity._zone.label_id == "Z1"

    site: Site = entity.coordinator_typed.site
    assert site is not None
    assert str(site.product) == "Hydromotrix - Mixte Eau chaude instantanée (Condensation - 32 kW)"
    assert site.serial_number == "A1AB12345"
    assert site.name == "Somewhere"
    assert site.last_updated == datetime(2025, 1, 31, 10, 0, 41)
    # TODO: Add more assertions here with the data mocked in the test


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(mock_add_entities: AddEntitiesCallback):
    async_core_setup_entry_no_site_id(async_setup_entry, mock_add_entities)
