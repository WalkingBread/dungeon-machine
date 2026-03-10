from uuid import UUID
from fastapi import WebSocket
from enum import Enum, auto

class MessageType(Enum):    
    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()
    
    PLAYER_JOINED = auto()
    CHARACTER_CREATED = auto()
    GAME_STARTED = auto()
    AUTHENTICATE = auto()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, dict[UUID, WebSocket]] = {}

    async def connect(self, session_id: UUID, player_id: UUID, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = {}
        self.active_connections[session_id][player_id] = websocket

    def disconnect(self, session_id: UUID, player_id: UUID):
        if session_id in self.active_connections:
            self.active_connections[session_id].pop(player_id, None)
        
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def session_broadcast(self, session_id: UUID, message: dict):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id].values():
                await connection.send_json(message)