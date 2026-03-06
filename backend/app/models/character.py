from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class CreateCharacterRequest(BaseModel):
    player_id: UUID
    name: str

class CreateCharacterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    health: int
    max_health: int
    money: int
    stats: dict[str, int] = Field(validation_alias="stats_dict")