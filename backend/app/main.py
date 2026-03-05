import uvicorn

from fastapi import FastAPI, HTTPException, Depends
from logic.game.session import SessionManager
from services.game import GameService, SessionNotFoundError, SessionFullError, PlayersNotReadyError
from pydantic import BaseModel

GLOBAL_SESSION_MANAGER = SessionManager()

def get_game_service():
    return GameService(GLOBAL_SESSION_MANAGER)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "dungeon machine"}

@app.post('/create-game')
def create_game(service: GameService = Depends(get_game_service)):
    session = service.create_game()
    return {"session_id": session.id}

class JoinRequest(BaseModel):
    username: str

@app.post('/session/{session_id}/join')
def join_game(session_id: str, data: JoinRequest, 
              service: GameService = Depends(get_game_service)):
    try:
        player = service.join_game(session_id, data.username)

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except SessionFullError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {'player_id': player.id}

class StartGameRequest(BaseModel):
    game_theme: str

@app.post('/session/{session_id}/start-game')
def start_game(session_id: str, data: StartGameRequest,
                     service: GameService = Depends(get_game_service)):
    try:
        service.start_game(session_id, data.game_theme)
    except PlayersNotReadyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': 'Game started.'}

class CreateCharacterRequest(BaseModel):
    player_id: str
    name: str

@app.post('/session/{session_id}/create-character')
def create_character(session_id: str, data: CreateCharacterRequest,
                     service: GameService = Depends(get_game_service)):
    character = service.create_character(session_id, data.player_id, data.name)
    return {}

PORT = 8000

if __name__ == '__main__':
    uvicorn.run(app, port=PORT)