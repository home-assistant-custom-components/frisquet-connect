import logging

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect_unofficial.entities.utils import get_device_info
from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class CoreResetSwitch(SwitchEntity, CoordinatorEntity):

    def __init__(self, coordinator: FrisquetConnectCoordinator, translation_key: str, suffix_id: str = None) -> None:
        super().__init__(coordinator)

        suffix = f"_{suffix_id}" if suffix_id else ""

        self._attr_unique_id = f"{coordinator.site.name}_reset_{translation_key}{suffix}"
        self._attr_has_entity_name = True
        self._attr_translation_key = translation_key
        self._attr_device_class = SwitchDeviceClass.SWITCH

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.coordinator)

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        pass

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        pass

    async def async_toggle(self, **kwargs):
        """Toggle the entity."""
        pass
