from custom_components.frisquet_connect_unofficial.const import ZoneMode, ZoneSelector
from custom_components.frisquet_connect_unofficial.domains.site.zone import Zone
from homeassistant.components.climate.const import (
    HVACMode,
    PRESET_NONE,
    PRESET_BOOST,
    PRESET_HOME,
    PRESET_AWAY,
    PRESET_COMFORT,
    PRESET_SLEEP,
    PRESET_ECO,
)


def get_hvac_and_preset_mode_for_a_zone(zone: Zone) -> tuple[list[HVACMode], str, HVACMode]:
    # TODO: Have flag to inform into the card => is_exemption = zone.detail.is_exemption_enabled

    # Inputs
    selector = zone.detail.selector
    mode = zone.detail.mode

    # Outputs
    available_preset_modes: list[str]
    hvac_mode: HVACMode
    preset_mode: str

    # AUTO
    if selector == ZoneSelector.AUTO:
        available_preset_modes = [PRESET_HOME, PRESET_AWAY]
        preset_mode = PRESET_HOME if mode == ZoneMode.COMFORT else PRESET_AWAY
        hvac_mode = HVACMode.AUTO

    # MANUAL HEAT - COMFORT_PERMANENT or REDUCED_PERMANENT
    available_preset_modes = [PRESET_COMFORT, PRESET_SLEEP]
    hvac_mode = HVACMode.HEAT
    if selector == ZoneSelector.COMFORT_PERMANENT:
        preset_mode = PRESET_COMFORT
    elif selector == ZoneSelector.REDUCED_PERMANENT:
        preset_mode = PRESET_SLEEP
    # MANUAL HEAT - FROST_PROTECTION
    elif selector == ZoneSelector.FROST_PROTECTION:
        available_preset_modes = [PRESET_ECO]
        preset_mode = PRESET_ECO
        hvac_mode = HVACMode.OFF
    # UNKNOW
    else:
        available_preset_modes = [PRESET_NONE]
        preset_mode = PRESET_NONE
        hvac_mode = HVACMode.OFF

    if zone.is_boost_available:
        available_preset_modes = [PRESET_BOOST, *available_preset_modes]
    return (available_preset_modes, preset_mode, hvac_mode)


def get_target_temperature(zone: Zone) -> float | None:
    mode = zone.detail.mode
    if mode == ZoneMode.COMFORT:
        return zone.detail.comfort_temperature
    elif mode == ZoneMode.REDUCED:
        return zone.detail.reduced_temperature
    elif mode == ZoneMode.FROST_PROTECTION:
        return zone.detail.frost_protection_temperature
    else:
        return None
