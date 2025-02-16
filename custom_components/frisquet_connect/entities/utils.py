from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect.const import DEVICE_MANUFACTURER, DEVICE_NAME, DOMAIN
from custom_components.frisquet_connect.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


# https://developers.home-assistant.io/docs/device_registry_index/
# TODO: Create a decorator for that
# TODO : move to CoreEntity and remove name field
def get_device_info(name: str, unique_id: str, coordinator: FrisquetConnectCoordinator) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, unique_id)},
        name=DEVICE_NAME,
        manufacturer=DEVICE_MANUFACTURER,
        model=coordinator.site.product,
        serial_number=coordinator.site.serial_number,
        via_device=(DOMAIN, coordinator.site.site_id),
    )
