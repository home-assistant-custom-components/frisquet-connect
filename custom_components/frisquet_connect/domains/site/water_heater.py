from custom_components.frisquet_connect.const import CoreEcsMode, EcsType
from custom_components.frisquet_connect.domains.model_base import ModelBase


class WaterHeater(ModelBase):
    _TYPE_ECS: int
    _MODE_ECS: dict

    def __init__(self, response_json: dict):
        super().__init__(response_json)

    @property
    def ecs_type(self) -> EcsType:
        return EcsType(self._TYPE_ECS)

    @property
    def ecs_mode(self) -> CoreEcsMode:
        return CoreEcsMode(self._MODE_ECS.get("id"))
