from homeassistant.components.climate.const import PRESET_AWAY, PRESET_HOME
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity

from custom_components.frisquet_connect.const import (
    SENSOR_ZONE_EXEMPTION_TRANSLATIONS_KEY,
    ZoneExemptionType,
)
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.entities.climate.utils import (
    get_hvac_and_preset_mode_for_a_zone,
)
from custom_components.frisquet_connect.entities.core_entity import CoreEntity


class ZoneExemptionEntity(CoreEntity, SensorEntity):
    def __init__(
        self,
        coordinator: FrisquetConnectCoordinator,
        zone_label_id: str,
    ) -> None:
        super().__init__(coordinator)

        self._zone_label_id = zone_label_id
        self._attr_unique_id = (
            f"{coordinator.data.site_id}_{SENSOR_ZONE_EXEMPTION_TRANSLATIONS_KEY}_{zone_label_id}"
        )
        self._attr_translation_key = SENSOR_ZONE_EXEMPTION_TRANSLATIONS_KEY
        self._attr_translation_placeholders = {"zone_name": self.zone.name}
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [exemption_type for exemption_type in ZoneExemptionType]

    @property
    def zone(self) -> Zone:
        return self.coordinator.data.get_zone_by_label_id(self._zone_label_id)

    def update(self) -> None:
        if not self.zone.detail.is_exemption_enabled:
            self._attr_native_value = ZoneExemptionType.NONE
            return

        _, preset_mode, _ = get_hvac_and_preset_mode_for_a_zone(self.zone)
        if preset_mode == PRESET_HOME:
            self._attr_native_value = ZoneExemptionType.COMFORT
        elif preset_mode == PRESET_AWAY:
            self._attr_native_value = ZoneExemptionType.REDUCED
        else:
            self._attr_native_value = ZoneExemptionType.NONE
