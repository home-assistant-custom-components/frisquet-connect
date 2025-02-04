from enum import Enum, StrEnum

from homeassistant.const import Platform

from homeassistant.components.climate.const import (
    PRESET_BOOST,
    PRESET_HOME,
    PRESET_AWAY,
    PRESET_COMFORT,
    PRESET_SLEEP,
    PRESET_ECO,
)

DOMAIN = "yet_another_frisquet_connect"
DEVICE_MANUFACTURER = "Frisquet"
PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR, Platform.WATER_HEATER, Platform.BUTTON]

BOOST_BUTTON_KEY = "boost"
EXEMPTION_BUTTON_KEY = "exemption"

### TRANSLATIONS KEYS
CLIMATE_TRANSLATIONS_KEY = "default_climate"
BOOST_BUTTON_TRANSLATIONS_KEY = "boost_button"
EXEMPTION_BUTTON_TRANSLATIONS_KEY = "exemption_button"

ALARM_CARD_NAME = "Alert"  # TODO : use translation
NO_ALARM = "Aucune alerte en cours"  # TODO : use translation

SANITARY_CONSUMPTION_LABEL = "Consommation Eau Chaude"  # TODO : use translation
HEATING_CONSUMPTION_LABEL = "Consommation Chauffage"  # TODO : use translation

INSIDE_THERMOMETER_LABEL = "Consommation Eau Chaude"  # TODO : use translation
OUTSIDE_THERMOMETER_LABEL = "Consommation Chauffage"  # TODO : use translation


class ZoneModeLabelOrder(StrEnum):
    COMFORT = "CONS_CONF"
    REDUCED = "CONS_RED"
    FROST_PROTECTION = "CONS_HG"


SANITARY_WATER_ORDER_LABEL = "MODE_ECS"
SELECTOR_ORDER_LABEL = "SELECTEUR"
EXEMPTION_ORDER_LABEL = "MODE_DERO"
BOOST_ORDER_LABEL = "ACTIVITE_BOOST"

## ENUMS


class AlarmType(Enum):
    NO_ALARM = 0
    DISCONNECTED = 5
    UNKNOWN = 9


class SanitaryWaterType(Enum):
    NORMAL = 0
    SOLAR = 1
    HEAT_PUMP = 2


class SanitaryWaterMode(Enum):  # StrEnum
    MAX = 0  # "Max"
    ECO = 1  # "Eco"
    ECO_TIMER = 2  # "Eco Timer"
    ECO_PLUS = 3  # "Eco+"
    ECO_PLUS_TIMER = 4  # "Eco+ Timer"
    STOP = 5  # "Stop"


class ZoneMode(Enum):  # StrEnum ?
    COMFORT = 6
    REDUCED = 7
    FROST_PROTECTION = 8


class ZoneSelector(Enum):
    AUTO = 5
    COMFORT_PERMANENT = 6
    REDUCED_PERMANENT = 7
    FROST_PROTECTION = 8


PRESET_MODE_ORDERS_MAPPING = {
    PRESET_BOOST: {"key_order": BOOST_ORDER_LABEL, "mode": ZoneMode.COMFORT},
    PRESET_HOME: {"key_order": EXEMPTION_ORDER_LABEL, "mode": ZoneMode.COMFORT},
    PRESET_AWAY: {"key_order": EXEMPTION_ORDER_LABEL, "mode": ZoneMode.REDUCED},
    PRESET_COMFORT: {"key_order": SELECTOR_ORDER_LABEL, "mode": ZoneMode.COMFORT},
    PRESET_SLEEP: {"key_order": SELECTOR_ORDER_LABEL, "mode": ZoneMode.REDUCED},
    PRESET_ECO: {"key_order": SELECTOR_ORDER_LABEL, "mode": ZoneMode.FROST_PROTECTION},
}
