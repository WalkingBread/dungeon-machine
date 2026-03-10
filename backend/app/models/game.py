from pydantic import BaseModel, ConfigDict, Field
from models.character import CharacterSchema
from typing import Optional
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
    auth_token: str = Field(validation_alias="auth_token")

class LeaveGameRequest(BaseModel):
    player_id: UUID
    auth_token: str

class StartGameRequest(BaseModel):
    game_theme: str

class PlayerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    player_id: UUID
    username: str
    status: str
    character: Optional[CharacterSchema] = None

class SessionStateResponse(BaseModel):
    session_id: UUID
    players: list[PlayerSchema]

    @classmethod
    def from_session(cls, session):
        players_data = []
        
        for p_id, player in session._players.items():
            char = session._player_characters.get(p_id)
            
            players_data.append(PlayerSchema(
                player_id=player.id,
                username=player.username,
                status=player.status.value,
                character=CharacterSchema.model_validate(char) if char else None
            ))

        return cls(session_id=session.id, players=players_data)