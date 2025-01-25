from custom_components.frisquet_connect.domains.model_base import ModelBase
from custom_components.frisquet_connect.domains.site.utils import convert_api_temperature_to_float


class Environment(ModelBase):
    _T_EXT:int
    
    def __init__(self, response_json: dict):
        super().__init__(response_json)
        
    @property
    def outside_temperature(self) -> float:
        return convert_api_temperature_to_float(self._T_EXT)
