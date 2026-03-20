from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from uuid import UUID
from connection import Connection
from connection.manager import ConnectionManager
from models.connection import (
    WebSocketMessage,
    AuthenticateRequest,
    InfoResponse,
    SessionStateResponse,
    ErrorResponse,
    PlayerLeftResponse,
    PlayerJoinedResponse,
    PlayerUpdateResponse
)
from logic.game.session import SessionManager
from services.game import GameService
from services.game.error import (
    SessionNotFoundError, 
    SessionFullError, 
    PlayersNotReadyError, 
    PlayerNotFoundError
)
from models.character import (
    CreateCharacterResponse, 
    CreateCharacterRequest, 
    CharacterSchema
)
from models.game import (
    CreateGameResponse, 
    JoinGameRequest, 
    JoinGameResponse, 
    StartGameRequest, 
    GetGameResponse,
    LeaveGameRequest,
    SessionStateSchema,
    PlayerSchema
)

router = APIRouter(
    prefix="/session",
    tags=["Sessions"]
)

GLOBAL_SESSION_MANAGER = SessionManager()

def get_game_service():
    return GameService(GLOBAL_SESSION_MANAGER)

CONNECTION_MANAGER = ConnectionManager()

class AuthFailedError(Exception):
    def __init__(self, message):
        super().__init__(message)

async def handshake_auth(connection: Connection, service: GameService):
    try:
        auth_data = await connection.receive_message(AuthenticateRequest)

        player = service.auth_player(
            connection.session_id, 
            connection.player_id, 
            auth_data.data.auth_token
        )

        await connection.send_message(InfoResponse(
            message=f"Player {player.username} authenticated successfully."
        ))
        return player
    except Exception as e:
        raise AuthFailedError(str(e))

@router.websocket('/connect/{session_id}/{player_id}')
async def game_session(websocket: WebSocket, session_id: UUID, player_id: UUID,
                       service: GameService = Depends(get_game_service)):
    
    connection = await CONNECTION_MANAGER.connect(session_id, player_id, websocket)
    
    try:
        try: 
            player = await handshake_auth(connection, service)
        except AuthFailedError as e:
            await connection.send_message(ErrorResponse(message=str(e)))
            await connection.close(1008)
            CONNECTION_MANAGER.disconnect(session_id, player_id)
            return
        
        await CONNECTION_MANAGER.session_broadcast(
            session_id, 
            PlayerJoinedResponse(
                player_data=PlayerSchema.model_validate(player)
            ),
            exclude=[connection]
        )

        session = service.get_session(session_id)
        session_state = SessionStateSchema.from_session(session)

        await connection.send_message(SessionStateResponse(data=session_state))

        while True:
            data = await connection.receive_any()
            print(data)
        

    except WebSocketDisconnect:
        CONNECTION_MANAGER.disconnect(session_id, player_id)
        await CONNECTION_MANAGER.session_broadcast(
            session_id, 
            PlayerLeftResponse(player_id=player_id)
        )

    except Exception as e:
        await connection.send_message(ErrorResponse(message=str(e)))


@router.post('/create', response_model=CreateGameResponse)
def create_game(service: GameService = Depends(get_game_service)):
    return service.create_game()

@router.get('/{session_id}', response_model=GetGameResponse)
def get_game(session_id: UUID, service: GameService = Depends(get_game_service)):
    try:
        session = service.get_session(session_id)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return session

@router.post('/{session_id}/join', response_model=JoinGameResponse)
def join_game(session_id: UUID, data: JoinGameRequest, 
              service: GameService = Depends(get_game_service)):
    try:
        player = service.join_game(session_id, data.username)

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except SessionFullError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return player


@router.post('/{session_id}/leave')
def leave_game(session_id: UUID, data: LeaveGameRequest, 
               service: GameService = Depends(get_game_service)):
    try:
        service.leave_game(session_id, data.player_id, data.auth_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {'message': 'Player left.'}


@router.post('/{session_id}/start-game')
def start_game(session_id: UUID, data: StartGameRequest,
                     service: GameService = Depends(get_game_service)):
    try:
        service.start_game(session_id, data.game_theme)

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except PlayersNotReadyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': 'Game started.'}


@router.post('/{session_id}/create-character', response_model=CreateCharacterResponse)
async def create_character(session_id: UUID, data: CreateCharacterRequest,
                     service: GameService = Depends(get_game_service)):
    try:
        player_id = data.player_id

        character = service.create_character(session_id, player_id, data.auth_token, data.name)

        player_data = PlayerSchema.model_validate(
            service.get_session(session_id).get_player(player_id)
        )
        player_data.character = CharacterSchema.model_validate(character)

        await CONNECTION_MANAGER.session_broadcast(
            session_id, 
            PlayerUpdateResponse(player_data=player_data)
        )

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return character