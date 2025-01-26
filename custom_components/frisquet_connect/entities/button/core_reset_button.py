import logging
from homeassistant.components.button import ButtonEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.frisquet_connect.domains.site.site import Site
from custom_components.frisquet_connect.domains.site.zone import Zone
from custom_components.frisquet_connect.services.frisquet_connect_coordinator import FrisquetConnectCoordinator


LOGGER = logging.getLogger(__name__)


class CoreResetButton(ButtonEntity, CoordinatorEntity):
    _site: Site

    def __init__(self, coordinator: FrisquetConnectCoordinator, suffix_id: str) -> None:
        super().__init__(coordinator)

        self._site = coordinator.site

        self._attr_unique_id = f"{self._site.name}_reset_{suffix_id}"
        self._attr_has_entity_name = True
        self._attr_name = f"Handle {suffix_id} button"

    @property
    def icon(self) -> str | None:
        return "mdi:cancel"

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    # TODO: Implement the action to reset
