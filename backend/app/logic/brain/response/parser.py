from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from logic.brain.model.request import (
    StoryUpdate, 
    AddCharacter, 
    ChangeHealth,
    DeleteCharacter,
    StatisticType, 
    ActionState, 
    RollRequest, 
    FinalSummary,
    StoryIntroduction,
    SceneUpdate
)
from logic.brain.dto.brain import (
    SceneIntroductionDto, 
    DiceRollRequestDto, 
    FinalActionDescDto, 
    ActionStateDto,
    SceneDescriptionDto
)
from logic.character.stat import StatType
from logic.game.event import (
    GameEvent, HealthEvent, AddCharacterEvent, RemoveCharacterEvent
)

T = TypeVar("T")

class BaseResponseParser(ABC, Generic[T]):

    @abstractmethod
    def parse(self, response_content) -> T:
        pass

    def _map_to_game_events(self, llm_events) -> list[GameEvent]:
        game_events = []
        for event in llm_events:
            match event:
                case AddCharacter(character_name=name, health_amount=hp):
                    game_events.append(AddCharacterEvent(character_name=name, health_points=hp))

                case ChangeHealth(character_name=name, health_amount=change):
                    game_events.append(HealthEvent(character_name=name, health_change=change))

                case DeleteCharacter(character_name=name):
                    game_events.append(RemoveCharacterEvent(character_name=name))
                case _:
                    raise ValueError(f"Unknown event type in LLM Response Parser: {type(event)}")

        return game_events

    def _map_stat_type(self, llm_stat: StatisticType) -> StatType | None:
        if llm_stat == StatisticType.NO_STATISTIC:
            return None

        try:
            return StatType[llm_stat.name]
        except KeyError:
            return None
        
class StoryUpdateParser(BaseResponseParser[SceneIntroductionDto]):

    def parse(self, response_content: StoryUpdate) -> SceneIntroductionDto:
        return SceneIntroductionDto(
            scene_intro=response_content.new_story_segment, 
            game_events=self._map_to_game_events(response_content.engine_events)
        )
    
class StoryIntroParser(BaseResponseParser[str]):
        
    def parse(self, response_content: StoryIntroduction) -> str:
        return response_content.story_segment
    
class ActionStateParser(BaseResponseParser[ActionStateDto]):

    def parse(self, response_content: ActionState) -> ActionStateDto:
        return ActionStateDto(
            narrative=response_content.narrative,
            game_events=self._map_to_game_events(response_content.engine_events),
            state=response_content.state
        )
    
class SceneUpdateParser(BaseResponseParser[SceneUpdate]):

    def parse(self, response_content: SceneUpdate) -> SceneDescriptionDto:
        return ActionStateDto(
            narrative=response_content.narrative,
            game_events=self._map_to_game_events(response_content.engine_events),
        )
        
class RollRequirementParser(BaseResponseParser[DiceRollRequestDto]):

    def parse(self, response_content: RollRequest) -> DiceRollRequestDto:
        return DiceRollRequestDto(
            requested_stat=self._map_stat_type(response_content.statistic)
        )

class FinalSummaryParser(BaseResponseParser[FinalActionDescDto]):

    def parse(self, response_content: FinalSummary) -> FinalActionDescDto:
        return FinalActionDescDto(
            desc=response_content.final_story,
        )