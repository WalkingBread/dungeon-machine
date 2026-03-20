from fastapi.websockets import WebSocket
from fastapi.encoders import jsonable_encoder
from models.connection import WebSocketMessage
from pydantic import BaseModel, TypeAdapter
from uuid import UUID

MESSAGE_ADAPTER = TypeAdapter(WebSocketMessage)

class Connection:
    def __init__(self, websocket: WebSocket, session_id: UUID, player_id: UUID):
        self.websocket = websocket
        self.session_id = session_id
        self.player_id = player_id

    async def close(self, code=1000):
        await self.websocket.close(code)

    async def send_message(self, message: WebSocketMessage):
        payload = jsonable_encoder(message)
        await self.websocket.send_json(payload)

    async def receive_message(self, model: type[BaseModel]):
        raw_data = await self.receive_any()
        return model.model_validate(raw_data)
    
    async def receive_any_message(self):
        raw_data = await self.receive_any
        return MESSAGE_ADAPTER.validate_python(raw_data)
    
    async def receive_any(self):
        return await self.websocket.receive_json()
    