import uvicorn

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from logic.game.session import SessionManager
from services.game import GameService, SessionNotFoundError, SessionFullError, PlayersNotReadyError, PlayerNotFoundError
from models.character import CreateCharacterResponse, CreateCharacterRequest
from models.game import CreateGameResponse, JoinGameRequest, JoinGameResponse, StartGameRequest, GetGameResponse
from uuid import UUID

GLOBAL_SESSION_MANAGER = SessionManager()

def get_game_service():
    return GameService(GLOBAL_SESSION_MANAGER)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "dungeon machine"}

@app.post('/create-game', response_model=CreateGameResponse)
def create_game(service: GameService = Depends(get_game_service)):
    return service.create_game()

@app.get('/session/{session_id}', response_model=GetGameResponse)
def get_game(session_id: UUID, service: GameService = Depends(get_game_service)):
    try:
        session = service.get_session(session_id)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return session

@app.post('/session/{session_id}/join', response_model=JoinGameResponse)
def join_game(session_id: UUID, data: JoinGameRequest, 
              service: GameService = Depends(get_game_service)):
    try:
        player = service.join_game(session_id, data.username)

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except SessionFullError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return player


@app.post('/session/{session_id}/start-game')
def start_game(session_id: UUID, data: StartGameRequest,
                     service: GameService = Depends(get_game_service)):
    try:
        service.start_game(session_id, data.game_theme)

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except PlayersNotReadyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': 'Game started.'}


@app.post('/session/{session_id}/create-character', response_model=CreateCharacterResponse)
def create_character(session_id: UUID, data: CreateCharacterRequest,
                     service: GameService = Depends(get_game_service)):
    try:
        character = service.create_character(session_id, data.player_id, data.name)

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return character

PORT = 8000

if __name__ == '__main__':
    uvicorn.run(app, port=PORT)