import logging

from homeassistant.components.button import ButtonEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect_unofficial.services.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


LOGGER = logging.getLogger(__name__)


class CoreResetButton(ButtonEntity, CoordinatorEntity):

    def __init__(
        self, coordinator: FrisquetConnectCoordinator, translation_key: str, suffix_id: str = None
    ) -> None:
        super().__init__(coordinator)

        suffix = f"_{suffix_id}" if suffix_id else ""

        self._attr_unique_id = f"{coordinator.site.name}_reset_{translation_key}{suffix}"
        self._attr_has_entity_name = True
        self._attr_translation_key = translation_key

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    # TODO: Implement the action to reset
