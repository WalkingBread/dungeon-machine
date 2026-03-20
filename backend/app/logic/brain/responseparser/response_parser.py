from logic.brain.modelmanager.request_structures import StoryUpdate, AddCharacter, ChangeHealth, \
    DeleteCharacter, StatisticType, ActionDecision, RollRequirement, RollConsequence, FinalSummary
from logic.brain.dtos import SceneIntroductionDto, DiceRollRequestDto, FinalActionOutcomeDto
from logic.character.stat import StatType
from logic.game.game_event import GameEvent, HealthEvent, AddCharacterEvent, RemoveCharacterEvent


class ResponseParser:

    def parse_story_update(self, story_update: StoryUpdate) -> SceneIntroductionDto:
        return SceneIntroductionDto(scene_intro=story_update.new_story_segment,
                                    game_events=self._map_to_game_events(story_update.engine_events))

    def parse_action_decision(self, decision: ActionDecision) -> bool:
        if decision.decision == "CONTINUE":
            return True
        elif decision.decision == "FINISH":
            return False
        else:
            raise ValueError(f"Unknown decision in LLM Response Parser: {decision}")

    def parse_roll_requirement(self, requirement: RollRequirement) -> DiceRollRequestDto:
        return DiceRollRequestDto(attempt_desc=requirement.intro,
                                  requested_stat=self._map_stat_type(requirement.statistic))

    def parse_roll_consequence(self, consequence: RollConsequence) -> str:
        return consequence.desc

    def parse_final_summary(self, summary: FinalSummary) -> FinalActionOutcomeDto:
        return FinalActionOutcomeDto(outcome_desc=summary.final_story,
                                     game_events=self._map_to_game_events(summary.final_events))


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
