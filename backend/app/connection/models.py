from pydantic import BaseModel, ConfigDict, Field
from connection.message import MessageType
from models.game import SessionStateSchema, PlayerSchema
from models.character import CharacterSchema
from typing import Literal, Union, Annotated
from uuid import UUID

class AuthenticateData(BaseModel):
    auth_token: str

class AuthenticateRequest(BaseModel):
    type: Literal[MessageType.AUTHENTICATE] = MessageType.AUTHENTICATE
    data: AuthenticateData

class SessionStateResponse(BaseModel):
    type: Literal[MessageType.SESSION_STATE] = MessageType.SESSION_STATE
    data: SessionStateSchema

class InfoResponse(BaseModel):
    type: Literal[MessageType.INFO] = MessageType.INFO
    message: str

class ErrorResponse(BaseModel):
    type: Literal[MessageType.ERROR] = MessageType.ERROR
    message: str

class PlayerJoinedResponse(BaseModel):
    type: Literal[MessageType.PLAYER_JOINED] = MessageType.PLAYER_JOINED
    player_data: PlayerSchema

class PlayerLeftResponse(BaseModel):
    type: Literal[MessageType.PLAYER_LEFT] = MessageType.PLAYER_LEFT
    player_id: UUID

class PlayerUpdateResponse(BaseModel):
    type: Literal[MessageType.PLAYER_UPDATE] = MessageType.PLAYER_UPDATE
    player_data: PlayerSchema

WebSocketMessage = Annotated[
    Union[
        AuthenticateRequest, 
        SessionStateResponse,
        InfoResponse,
        ErrorResponse,
        PlayerLeftResponse,
        PlayerJoinedResponse,
        PlayerUpdateResponse
    ], 
    Field(discriminator='type')
]