from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated
from enum import Enum, auto

class AddCharacter(BaseModel):
    event_type: Literal["add_character"] = Field(
        default="add_character",
        description="Creates a new character entry."
    )
    character_name: str = Field(..., description="Unique name of the character (ex. 'Orc 1').")
    health_amount: int = Field(..., gt=0, description="The initial value of character's health.")

class ChangeHealth(BaseModel):
    event_type: Literal["change_health"] = Field(
        default="change_health",
        description="Adjusts health of an existing character."
    )
    character_name: str = Field(..., description="Target character's name.")
    health_amount: int = Field(..., description="The change to the character's health that should be done, negative values means decrement.")

class DeleteCharacter(BaseModel):
    event_type: Literal["delete_character"] = Field(
        default="delete_character",
        description="Removes a character from the state."
    )
    character_name: str = Field(..., description="Target character's name.")

GameEvent = Annotated[
    Union[AddCharacter, ChangeHealth, DeleteCharacter],
    Field(discriminator="event_type")
]

class StoryUpdate(BaseModel):
    new_story_segment: str = Field(
        ...,
        description="The next part of the narrative based on the previous story segment."
    )
    engine_events: list[GameEvent] = Field(
        default_factory=list,
        description="The technical state changes triggered by this story segment.",
    )

class StatisticType(Enum):
    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()
    NO_STATISTIC = auto()
    STRENGTH = auto()
    AGILITY = auto()
    INTELLIGENCE = auto()
    LUCK = auto()
    CHARISMA = auto()

class DiceRoll(BaseModel):
    name: str = Field(default="dice_roll")
    character_name: str = Field(..., description="The character to perform the action.")
    statistic: StatisticType = Field(
        ...,
        description="The stat to use. Use NO_STAT for flat rolls with no modifiers."
    )

class PlayerActionOutcome(BaseModel):
    description: str = Field(
        ...,
        description="A very short summary of the triggering event(s) (e.g., 'The guard notices you' or 'A heavy stone door slides shut')."
    )
    rolls: list[DiceRoll] = Field(
        default_factory=list,
        description="The physical tests required to respond to this event."
    )