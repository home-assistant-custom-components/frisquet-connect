import pytest
from custom_components.frisquet_connect.const import (
    CLIMATE_TRANSLATIONS_KEY,
    SENSOR_ALARM_TRANSLATIONS_KEY,
    SENSOR_HEATING_CONSUMPTION_TRANSLATIONS_KEY,
    SENSOR_INSIDE_THERMOMETER_TRANSLATIONS_KEY,
    SENSOR_OUTSIDE_THERMOMETER_TRANSLATIONS_KEY,
    SENSOR_SANITARY_CONSUMPTION_TRANSLATIONS_KEY,
    SWITCH_BOOST_TRANSLATIONS_KEY,
    SWITCH_EXEMPTION_TRANSLATIONS_KEY,
    WATER_HEATER_TRANSLATIONS_KEY,
)
from tests.utils import read_translation_file
from homeassistant.const import Platform


@pytest.mark.asyncio
async def test_async_sanity_check_comparison():
    default_translation = read_translation_file()
    fr_translation = read_translation_file("fr")

    recursive_check(default_translation, fr_translation)


@pytest.mark.asyncio
async def test_async_sanity_check_missing_key():
    default_translation = read_translation_file()
    default_entities = default_translation.get("entity")
    types = {
        Platform.CLIMATE: [CLIMATE_TRANSLATIONS_KEY],
        Platform.WATER_HEATER: [WATER_HEATER_TRANSLATIONS_KEY],
        Platform.SENSOR: [
            SENSOR_ALARM_TRANSLATIONS_KEY,
            SENSOR_INSIDE_THERMOMETER_TRANSLATIONS_KEY,
            SENSOR_OUTSIDE_THERMOMETER_TRANSLATIONS_KEY,
            SENSOR_HEATING_CONSUMPTION_TRANSLATIONS_KEY,
            SENSOR_SANITARY_CONSUMPTION_TRANSLATIONS_KEY,
        ],
        Platform.SWITCH: [SWITCH_BOOST_TRANSLATIONS_KEY, SWITCH_EXEMPTION_TRANSLATIONS_KEY],
    }

    for platform, platform_entities in default_entities.items():
        for entity in platform_entities.keys():
            assert entity in types[platform]


def recursive_check(default_translation, fr_translation):
    for key in default_translation.keys():
        if isinstance(default_translation[key], dict):
            recursive_check(default_translation[key], fr_translation[key])
        else:
            assert key in fr_translation.keys()
