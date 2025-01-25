from enum import Enum
from custom_components.frisquet_connect.const import ZoneMode, ZoneSelector
from custom_components.frisquet_connect.domains.model_base import ModelBase
from custom_components.frisquet_connect.domains.site.utils import convert_api_temperature_to_float


class ZoneDetail(ModelBase):
    MODE: ZoneMode
    SELECTEUR: ZoneSelector
    TAMB: int  # current temperature
    CAMB: int  # target temperature
    DERO: bool
    CONS_RED: int  # consigne reduite
    CONS_CONF: int  # consigne confort
    CONS_HG: int  # consigne hors gel
    ACTIVITE_BOOST: bool

    def __init__(self, response_json: dict):
        super().__init__(response_json)

    @property
    def current_temperature(self) -> float:
        return convert_api_temperature_to_float(self.TAMB)

    @property
    def target_temperature(self) -> float:
        return convert_api_temperature_to_float(self.CAMB)

    @property
    def is_exemption_enabled(self) -> bool:
        return self.DERO

    @property
    def reduced_temperature(self) -> float:
        return convert_api_temperature_to_float(self.CONS_RED)

    @property
    def comfort_temperature(self) -> float:
        return convert_api_temperature_to_float(self.CONS_CONF)

    @property
    def frost_protection_temperature(self) -> float:
        return convert_api_temperature_to_float(self.CONS_HG)

    @property
    def is_boosting(self) -> bool:
        return self.ACTIVITE_BOOST

    @property
    def mode(self) -> ZoneMode:
        return ZoneMode(self.MODE)

    @property
    def selector(self) -> ZoneSelector:
        return ZoneSelector(self.SELECTEUR)
