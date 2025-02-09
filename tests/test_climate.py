from datetime import datetime
import pytest

from tests.utils import mock_endpoints, unstub_all

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.climate.const import (
    HVACMode,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_SLEEP,
    PRESET_HOME,
    PRESET_AWAY,
    PRESET_ECO,
    PRESET_ACTIVITY,
)

from custom_components.frisquet_connect_unofficial.climate import async_setup_entry
from custom_components.frisquet_connect_unofficial.const import (
    DOMAIN,
    SanitaryWaterMode,
    SanitaryWaterType,
    ZoneMode,
    ZoneSelector,
)
from custom_components.frisquet_connect_unofficial.domains.site.site import Site
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from custom_components.frisquet_connect_unofficial.entities.climate.default_climate import (
    DefaultClimateEntity,
)
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_service import (
    FrisquetConnectService,
)
from tests.conftest import async_core_setup_entry_with_site_id_mutated


async def async_init_climate(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    # Initialize the mocks
    mock_endpoints()

    # Test the feature
    service = FrisquetConnectService(mock_entry.data.get("email"), mock_entry.data.get("password"))
    mock_hass.data[DOMAIN] = {mock_entry.unique_id: service}
    await async_setup_entry(mock_hass, mock_entry, mock_add_entities)

    # Assertions
    mock_add_entities.assert_called_once()
    entities = mock_add_entities.call_args[0][0]

    assert len(entities) == 1
    assert isinstance(entities[0], DefaultClimateEntity)

    return entities


@pytest.mark.asyncio
async def test_async_setup_entry_success(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    entities = await async_init_climate(mock_hass, mock_entry, mock_add_entities)

    entity: DefaultClimateEntity = entities[0]
    await entity.async_update()

    zone: Zone = entity._zone
    assert zone is not None
    assert entity._zone.label_id == "Z1"

    # SITE
    site: Site = entity.coordinator_typed.site
    assert site is not None
    assert str(site.product) == "Hydromotrix - Mixte Eau chaude instantanée (Condensation - 32 kW)"
    assert site.serial_number == "A1AB12345"
    assert site.name == "Somewhere"
    assert site.site_id == "12345678901234"
    assert site.last_updated == datetime(2025, 1, 31, 10, 0, 41)
    assert site.external_temperature == 3.4

    # SITE.DETAIL
    assert site.detail is not None
    assert site.detail.current_boiler_timestamp == datetime(2025, 1, 31, 10, 3, 40)
    assert site.detail.is_boiler_standby == False
    assert site.detail.is_heat_auto_mode == True

    # SITE.WATER_HEATER
    assert site.water_heater is not None
    assert site.water_heater.sanitary_water_type == SanitaryWaterType.NORMAL
    assert site.water_heater.sanitary_water_mode == SanitaryWaterMode.ECO_TIMER

    # SITE.ZONES
    assert site.zones is not None
    assert len(site.zones) == 1
    zone_not_found = site.get_zone_by_label_id("Z2")
    assert zone_not_found is None

    zone: Zone = site.zones[0]
    zone_expected = site.get_zone_by_label_id(zone.label_id)
    assert zone == zone_expected

    assert zone.name == "Zone 1"
    assert zone.label_id == "Z1"
    assert zone.is_boost_available == True

    # SITE.ZONES[0].DETAIL
    assert zone.detail is not None
    assert zone.detail.current_temperature == 17.0
    assert zone.detail.target_temperature == 18.5
    assert zone.detail.is_exemption_enabled == True
    assert zone.detail.comfort_temperature == 20.0
    assert zone.detail.reduced_temperature == 18.5
    assert zone.detail.frost_protection_temperature == 8.0
    assert zone.detail.is_boosting == False
    assert zone.detail.mode == ZoneMode.REDUCED
    assert zone.detail.selector == ZoneSelector.AUTO

    # SITE.SANITARY_WATER
    assert len(site.available_sanitary_water_modes) == 4
    for mode in site.available_sanitary_water_modes:
        assert mode in SanitaryWaterMode

    # SITE.ALARMS
    assert len(site.alarms) == 0

    unstub_all()


@pytest.mark.asyncio
async def test_climate_set_preset_mode(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    entities = await async_init_climate(mock_hass, mock_entry, mock_add_entities)

    entity: DefaultClimateEntity = entities[0]
    await entity.async_update()

    await entity.async_set_preset_mode(PRESET_BOOST)
    await entity.async_set_preset_mode(PRESET_HOME)
    await entity.async_set_preset_mode(PRESET_AWAY)
    await entity.async_set_preset_mode(PRESET_COMFORT)
    await entity.async_set_preset_mode(PRESET_SLEEP)
    await entity.async_set_preset_mode(PRESET_ECO)

    unstub_all()


@pytest.mark.asyncio
async def test_climate_set_invalid_preset_mode(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    entities = await async_init_climate(mock_hass, mock_entry, mock_add_entities)

    entity: DefaultClimateEntity = entities[0]
    with pytest.raises(ValueError):
        await entity.async_set_preset_mode(PRESET_ACTIVITY)

    unstub_all()


@pytest.mark.asyncio
async def test_climate_set_hvac_mode(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    entities = await async_init_climate(mock_hass, mock_entry, mock_add_entities)

    entity: DefaultClimateEntity = entities[0]
    await entity.async_update()

    await entity.async_set_hvac_mode(HVACMode.AUTO)
    await entity.async_set_hvac_mode(HVACMode.HEAT)
    await entity.async_set_hvac_mode(HVACMode.OFF)

    unstub_all()


@pytest.mark.asyncio
async def test_climate_set_invalid_hvac_mode(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    entities = await async_init_climate(mock_hass, mock_entry, mock_add_entities)

    entity: DefaultClimateEntity = entities[0]
    with pytest.raises(ValueError):
        await entity.async_set_hvac_mode(HVACMode.COOL)

    unstub_all()


@pytest.mark.asyncio
async def test_climate_set_temperature(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    entities = await async_init_climate(mock_hass, mock_entry, mock_add_entities)

    entity: DefaultClimateEntity = entities[0]
    await entity.async_set_temperature(temperature=18.0)

    unstub_all()


@pytest.mark.asyncio
async def test_async_setup_entry_no_site_id(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    await async_core_setup_entry_with_site_id_mutated(async_setup_entry, mock_add_entities, mock_hass, mock_entry)

    unstub_all()


@pytest.mark.asyncio
async def test_async_setup_entry_site_id_not_found(
    mock_hass: HomeAssistant, mock_entry: ConfigEntry, mock_add_entities: AddEntitiesCallback
):
    await async_core_setup_entry_with_site_id_mutated(
        async_setup_entry, mock_add_entities, mock_hass, mock_entry, "not_found"
    )

    unstub_all()
