from fastapi import APIRouter, HTTPException, Depends

from services.dice.dice import DiceService
from logic.dice.type import DiceType
from models.dice import RollDiceResponse

router = APIRouter(
    prefix="/dice",
    tags=["Dice"]
)

def get_dice_service() -> DiceService:
    return DiceService()

@router.get('/roll/{dice_type}', response_model=RollDiceResponse)
async def roll_dice(dice_type: DiceType, service: DiceService = Depends(get_dice_service)):
    return RollDiceResponse(roll_outcome=service.roll_dice(dice_type))