from datetime import datetime
import pytest

from tests.utils import mock_endpoints

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.frisquet_connect_unofficial.climate import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import DOMAIN
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.climate.default_climate import DefaultClimateEntity
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import FrisquetConnectService
from tests.conftest import async_core_setup_entry_no_site_id


@pytest.mark.asyncio
async def test_async_setup_entry_success(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    # Initialize the mocks
    mock_endpoints()

    # Test the feature
    service = FrisquetConnectService(mock_entry)
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: service}
    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

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
    assert site.external_temperature == 3.4
    # TODO: Add more assertions here with the data mocked in the test


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    await async_core_setup_entry_no_site_id(async_setup_entry, mock_add_entities, mock_hass, mock_entry)
