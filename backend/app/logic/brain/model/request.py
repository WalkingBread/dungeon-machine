from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated
from enum import Enum, auto

class AddCharacter(BaseModel):
    event_type: Literal["add_character"] = "add_character"
    character_name: str = Field(..., description="The entering character's name.")
    health_amount: int = Field(..., gt=0, description="Initial health.")

class DeleteCharacter(BaseModel):
    event_type: Literal["delete_character"] = "delete_character"
    character_name: str = Field(..., description="The target character's name.")

class ChangeHealth(BaseModel):
    event_type: Literal["change_health"] = "change_health"
    character_name: str = Field(..., description="The target character's name.")
    health_amount: int = Field(..., description="Change value (negative = damage).")

ActionEvent = Union[
    ChangeHealth
]

SceneSettingEvent = Annotated[
    Union[AddCharacter, DeleteCharacter],
    Field(discriminator="event_type")
]

class StoryIntroduction(BaseModel):
    story_segment: str = Field(..., description="Introduction to the story.")

class StoryUpdate(BaseModel):
    new_story_segment: str = Field(..., description="The next part of the narrative.")
    engine_events: list[SceneSettingEvent] = Field(default_factory=list)

class ActionState(BaseModel):
    narrative: str = Field(..., description='Narrative after player input or dice roll.')
    engine_events: list[ActionEvent] = Field(default_factory=list, description="A list of events that occur in this segment of action.")
    state: Literal["INPUT", "ROLL", "FINISH"] = Field(..., description="What should player do next?")

class StatisticType(Enum):
    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()
    NO_STATISTIC = auto()
    STRENGTH = auto()
    AGILITY = auto()
    INTELLIGENCE = auto()
    LUCK = auto()
    CHARISMA = auto()

class RollRequirement(BaseModel):
    statistic: StatisticType = Field(
        ...,
        description="The stat to use. Use NO_STATISTIC for flat rolls."
    )
    intro: str = Field(..., description="Suspenseful intro sentence before the roll.")


class RollConsequence(BaseModel):
    desc: str = Field(..., description="One-sentence physical result of the dice roll.")

class FinalSummary(BaseModel):
    final_story: str = Field(..., description="The cohesive 2-3 sentence final summary of the player action")
