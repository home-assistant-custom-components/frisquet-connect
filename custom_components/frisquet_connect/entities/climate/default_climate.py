import logging
from custom_components.frisquet_connect.const import (
    CLIMATE_TRANSLATIONS_KEY,
    ZoneSelector,
)
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.entities.climate.utils import (
    get_hvac_and_preset_mode_for_a_zone,
    get_target_temperature,
)
from custom_components.frisquet_connect.entities.utils import get_device_info
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_SLEEP,
    PRESET_HOME,
    PRESET_AWAY,
    PRESET_ECO,
)

from custom_components.frisquet_connect.utils import log_methods

_LOGGER = logging.getLogger(__name__)


@log_methods
class DefaultClimateEntity(ClimateEntity, CoordinatorEntity):
    _zone_label_id: str

    def __init__(self, coordinator: FrisquetConnectCoordinator, zone_label_id: str) -> None:
        super().__init__(coordinator)
        _LOGGER.debug(f"Creating Climate entity for zone {zone_label_id}")

        self._zone_label_id = zone_label_id

        self._attr_unique_id = f"{coordinator.site.name}_{zone_label_id}"
        self._attr_has_entity_name = True
        self._attr_translation_key = CLIMATE_TRANSLATIONS_KEY
        self._attr_translation_placeholders = {"zone_name": self.zone.name}

        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
        self._attr_hvac_modes = [HVACMode.AUTO, HVACMode.HEAT, HVACMode.OFF]

        self._attr_temperature_unit = "°C"
        self._attr_target_temperature_low = 5
        self._attr_target_temperature_high = 25
        _LOGGER.debug(f"Climate entity for zone {zone_label_id} created")

    @property
    def coordinator_typed(self) -> FrisquetConnectCoordinator:
        return self.coordinator

    @property
    def zone(self) -> Zone:
        return self.coordinator_typed.site.get_zone_by_label_id(self._zone_label_id)

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.name, self.unique_id, self.coordinator)

    @property
    def icon(self) -> str | None:
        return "mdi:home-thermometer-outline"

    @property
    def should_poll(self) -> bool:
        return True

    async def async_set_hvac_mode(self, hvac_mode):
        selector: ZoneSelector
        if hvac_mode == HVACMode.AUTO:
            selector = ZoneSelector.AUTO
        elif hvac_mode == HVACMode.HEAT:
            if self.preset_mode == PRESET_HOME:
                selector = ZoneSelector.COMFORT_PERMANENT
            else:
                selector = ZoneSelector.REDUCED_PERMANENT
        elif hvac_mode == HVACMode.OFF:
            selector = ZoneSelector.FROST_PROTECTION
        else:
            _LOGGER.error(f"Unknown HVAC mode '{hvac_mode}'")
            raise ValueError(f"Unknown HVAC mode '{hvac_mode}'")

        coordinator: FrisquetConnectCoordinator = self.coordinator
        await coordinator.service.async_set_selector(self.coordinator_typed.site.site_id, self.zone, selector)

    async def async_set_preset_mode(self, preset_mode: str):
        current_zone = self.zone
        if preset_mode == PRESET_BOOST:
            # TODO: Only available when the zone is in COMFORT mode
            await self.coordinator_typed.service.async_enable_boost(self.coordinator_typed.site.site_id, self.zone)
        elif preset_mode == PRESET_HOME:
            # TODO: Only available when HVACMode is in AUTO mode and the zone is in REDUCED mode or BOOST mode
            # TODO: If boost is active, it must be disabled before
            await self.coordinator_typed.service.async_set_exemption(
                self.coordinator_typed.site.site_id, ZoneSelector.COMFORT_PERMANENT
            )
        elif preset_mode == PRESET_AWAY:
            # TODO: Only available when HVACMode is in AUTO mode and the zone is in COMFORT mode
            # TODO: If boost is active, it must be disabled before
            await self.coordinator_typed.service.async_set_exemption(
                self.coordinator_typed.site.site_id, ZoneSelector.REDUCED_PERMANENT
            )
        elif preset_mode == PRESET_COMFORT:
            # TODO: Only available when HVACMode is in HEAT mode
            await self.coordinator_typed.service.async_set_selector(
                self.coordinator_typed.site.site_id, current_zone, ZoneSelector.COMFORT_PERMANENT
            )
        elif preset_mode == PRESET_SLEEP:
            # TODO: Only available when HVACMode is in HEAT mode
            await self.coordinator_typed.service.async_set_selector(
                self.coordinator_typed.site.site_id, current_zone, ZoneSelector.REDUCED_PERMANENT
            )
        elif preset_mode == PRESET_ECO:
            # TODO: Only available when HVACMode is in OFF mode
            await self.coordinator_typed.service.async_set_selector(
                self.coordinator_typed.site.site_id, current_zone, ZoneSelector.FROST_PROTECTION
            )
        else:
            _LOGGER.error(f"Unknown preset mode '{preset_mode}'")
            raise ValueError(f"Unknown preset mode '{preset_mode}'")

    async def async_set_temperature(self, **kwargs):
        coordinator: FrisquetConnectCoordinator = self.coordinator
        await coordinator.service.async_set_temperature(
            self.coordinator_typed.site.site_id, self.zone, kwargs["temperature"]
        )

    async def async_update(self):
        (available_preset_modes, preset_mode, hvac_mode) = get_hvac_and_preset_mode_for_a_zone(self.zone)
        self._attr_preset_modes = available_preset_modes
        self._attr_preset_mode = preset_mode
        self._attr_hvac_mode = hvac_mode

        self._attr_current_temperature = self.zone.detail.current_temperature
        self._attr_target_temperature = self.zone.detail.target_temperature
        if self._attr_target_temperature != get_target_temperature(self.zone):
            _LOGGER.warning(
                f"Current target temperature '{self.zone.detail.target_temperature}' is not the same as the one predefined in the {self.zone.name}: '{get_target_temperature(self.zone)}'"
            )
