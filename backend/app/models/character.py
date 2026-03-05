from pydantic import BaseModel, ConfigDict, Field

class PlayerCharacterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    health: int
    max_health: int
    money: int
    stats: dict[str, int] = Field(validation_alias="stats_dict")