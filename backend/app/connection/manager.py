from uuid import UUID
from connection import Connection
from models.connection import WebSocketMessage
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

    def get_connection(self, session_id: UUID, player_id: UUID) -> Connection:
        session_conns = self.active_connections.get(session_id)
        if session_conns:
            return session_conns.get(player_id)
        return None

    async def session_broadcast(self, session_id: UUID, message: WebSocketMessage, exclude: list[Connection] = []):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id].values():
                if connection in exclude:
                    continue
                await connection.send_message(message)