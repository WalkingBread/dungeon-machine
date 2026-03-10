from pydantic import BaseModel, Field
from typing import Literal, Union

from logic.brain.modelmanager.request_structures import ChangeHealth, StatisticType


class ActionDecision(BaseModel):
    decision: Literal["CONTINUE", "FINISH"] = Field(..., description="Is a roll still needed?")

class RollRequirement(BaseModel):
    statistic: "StatisticType" = Field(
        ...,
        description="The stat to use. Use NO_STATISTIC for flat rolls."
    )
    intro: str = Field(..., description="Suspenseful intro sentence before the roll.")

class RollConsequence(BaseModel):
    desc: str = Field(..., description="One-sentence physical result of the dice roll.")

FinalEvent = Union[
    ChangeHealth
]

class FinalSummary(BaseModel):
    final_story: str = Field(..., description="The cohesive 2-3 sentence final narrative.")
    final_events: list[FinalEvent] = Field(default_factory=list, description="A list of optional events for the "
                                                                             "game engine to execute after "
                                                                             "player's action.")