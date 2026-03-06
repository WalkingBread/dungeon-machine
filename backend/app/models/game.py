from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class CreateGameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    session_id: UUID = Field(validation_alias="id")

class GetGameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    session_id: UUID = Field(validation_alias="id")

class JoinGameRequest(BaseModel):
    username: str

class JoinGameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    player_id: UUID = Field(validation_alias="id")

class StartGameRequest(BaseModel):
    game_theme: str