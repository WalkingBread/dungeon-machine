from pydantic import BaseModel, ConfigDict, Field

class RollDiceResponse(BaseModel):
    roll_outcome: int