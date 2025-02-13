from homeassistant.helpers.entity import DeviceInfo

from custom_components.frisquet_connect_unofficial.const import DEVICE_MANUFACTURER, DOMAIN
from custom_components.frisquet_connect_unofficial.devices.frisquet_connect_coordinator import (
    FrisquetConnectCoordinator,
)


def get_device_info(name: str, coordinator: FrisquetConnectCoordinator) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, coordinator.site.site_id)},
        name=name,
        manufacturer=DEVICE_MANUFACTURER,
        model=coordinator.site.product,
        serial_number=coordinator.site.serial_number,
    )
