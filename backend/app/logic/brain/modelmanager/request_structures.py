from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated
from enum import Enum, auto

class AddCharacter(BaseModel):
    event_type: Literal["add_character"] = "add_character"
    character_name: str = Field(..., description="The entering character's name.")
    health_amount: int = Field(..., gt=0, description="Initial health.")


class ChangeHealth(BaseModel):
    event_type: Literal["change_health"] = "change_health"
    character_name: str = Field(..., description="The target character's name.")
    health_amount: int = Field(..., description="Change value (negative = damage).")

class DeleteCharacter(BaseModel):
    event_type: Literal["delete_character"] = "delete_character"
    character_name: str = Field(..., description="The target character's name.")

class DiceRoll(BaseModel):
    event_type: Literal["dice_roll"] = "dice_roll"
    character_name: str = Field(..., description="The name of player's character that is supposed to roll.")
    statistic: "StatisticType" = Field(
        ...,
        description="The stat to use. Use NO_STATISTIC for flat rolls."
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

SceneSettingEvent = Annotated[
    Union[AddCharacter, ChangeHealth, DeleteCharacter],
    Field(discriminator="event_type")
]

ActionOutcomeEvent = Annotated[
    Union[ChangeHealth, DiceRoll],
    Field(discriminator="event_type")
]

class IndividualOutcome(BaseModel):
    description: str = Field(..., description="A complete description of the player's action outcome up to this point.")
    rolls: list[ActionOutcomeEvent] = Field(default_factory=list, description="A list of events related to the outcome of the "
                                                                              "player's action up to this point.")

class PlayerActionOutcomes(BaseModel):
    character_outcomes: dict[str, IndividualOutcome] = Field(
        default_factory=dict, # This prevents the crash
        description="A map of character names to their specific situational consequences."
    )

class StoryUpdate(BaseModel):
    new_story_segment: str = Field(..., description="The next part of the narrative.")
    engine_events: list[SceneSettingEvent] = Field(default_factory=list)