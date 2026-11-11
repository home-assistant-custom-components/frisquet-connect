from datetime import datetime


def convert_from_epoch_to_datetime(epoch: int) -> datetime:
    return datetime.fromtimestamp(epoch)


def convert_api_temperature_to_float(api_temperature: int) -> float | None:
    if api_temperature is None:
        return None
    return float(api_temperature) / 10.0


def convert_hass_temperature_to_int(hass_temperature: float) -> int | None:
    if hass_temperature is None:
        return None
    return int(hass_temperature * 10)
