from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated
from enum import Enum, auto

class AddCharacter(BaseModel):
    name: Literal["add_character"] = Field(
        default="add_character",
        description="Creates a new character entry."
    )
    character_name: str = Field(..., description="Unique name of the character (ex. 'Orc 1').")
    health_amount: int = Field(..., gt=0, description="The initial value of character's health.")

class ChangeHealth(BaseModel):
    name: Literal["change_health"] = Field(
        default="change_health",
        description="Adjusts health of an existing character."
    )
    character_name: str = Field(..., description="Target character's name.")
    health_amount: int = Field(..., description="The change to the character's health that should be done, negative values means decrement.")

class DeleteCharacter(BaseModel):
    name: Literal["delete_character"] = Field(
        default="delete_character",
        description="Removes a character from the state."
    )
    character_name: str = Field(..., description="Target character's name.")

GameEvent = Annotated[
    Union[AddCharacter, ChangeHealth, DeleteCharacter],
    Field(discriminator="name")
]

class StoryUpdate(BaseModel):
    new_story_segment: str = Field(
        ...,
        description="The next part of the narrative based on the user's input."
    )
    engine_events: list[GameEvent] = Field(
        default_factory=list,
        description="The technical state changes triggered by this story segment.",
    )

class StatType(Enum):
    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()
    NO_STAT = auto()
    STRENGTH = auto()
    AGILITY = auto()
    INTELLIGENCE = auto()
    LUCK = auto()
    CHARISMA = auto()

class DiceRoll(BaseModel):
    name: str = Field(default="dice_roll")
    character_name: str = Field(..., description="The character to perform the action.")
    statistic: StatType = Field(
        ...,
        description="The stat to use. Use NO_STAT for flat rolls with no modifiers."
    )

class RollDecision(BaseModel):
    rolls: list[DiceRoll] = Field(
        default_factory=list,
        description="List of required dice rolls. Empty if no action is required."
    )