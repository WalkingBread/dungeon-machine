from uuid import UUID
from connection import Connection
from connection.models import WebSocketMessage
from fastapi.websockets import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, dict[UUID, Connection]] = {}

    async def connect(self, session_id: UUID, player_id: UUID, websocket: WebSocket) -> Connection:
        await websocket.accept()

        connection = Connection(websocket, session_id, player_id)
        if session_id not in self.active_connections:
            self.active_connections[session_id] = {}
        self.active_connections[session_id][player_id] = connection

        return connection

    def disconnect(self, session_id: UUID, player_id: UUID):
        if session_id in self.active_connections:
            self.active_connections[session_id].pop(player_id, None)
        
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def session_broadcast(self, session_id: UUID, message: WebSocketMessage):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id].values():
                await connection.send_message(message)