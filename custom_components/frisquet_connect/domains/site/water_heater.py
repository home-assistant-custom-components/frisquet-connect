from custom_components.frisquet_connect.const import SanitaryWaterMode, SanitaryWaterType
from custom_components.frisquet_connect.domains.model_base import ModelBase


class WaterHeater(ModelBase):
    _TYPE_ECS: int
    _solaire: bool
    _MODE_ECS: dict
    _MODE_ECS_SOLAIRE: dict
    _MODE_ECS_PAC: dict

    def __init__(self, response_json: dict):
        super().__init__(response_json)

    @property
    def sanitary_water_type(self) -> SanitaryWaterType:
        return SanitaryWaterType(self._TYPE_ECS)

    @property
    def sanitary_water_mode(self) -> SanitaryWaterMode:
        if self.sanitary_water_type == SanitaryWaterType.NORMAL:
            return SanitaryWaterMode(self._MODE_ECS.get("id"))
        if self.sanitary_water_type == SanitaryWaterType.SOLAR:
            return SanitaryWaterMode(self._MODE_ECS_SOLAIRE.get("id"))
        if self.sanitary_water_type == SanitaryWaterType.HEAT_PUMP:
            return SanitaryWaterMode(self._MODE_ECS_PAC.get("id"))
