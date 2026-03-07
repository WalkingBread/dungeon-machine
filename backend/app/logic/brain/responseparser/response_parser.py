from logic.brain.player_action_outcome import PlayerActionOutcome
from logic.brain.modelmanager.request_structures import StoryUpdate, AddCharacter, ChangeHealth, \
    DeleteCharacter, DiceRoll, StatisticType, PlayerActionOutcomes
from logic.character.stat import StatType
from logic.game.game_event import GameEvent, HealthEvent, DiceEvent, AddCharacterEvent, RemoveCharacterEvent
from logic.game.scene import SceneDescriptionSequence


class ResponseParser:

    def parse_to_scene_setting(self, story_update: StoryUpdate) \
            -> tuple[SceneDescriptionSequence, list[GameEvent]]:

        sequence = SceneDescriptionSequence(content=story_update.new_story_segment)
        events = self._map_to_game_events(story_update.engine_events)

        return sequence, events

    def parse_to_player_action_outcome(self, action_outcomes: PlayerActionOutcomes) \
            -> list[PlayerActionOutcome]:

        results = []

        for char_name, outcome in action_outcomes.character_outcomes.items():
            game_events = self._map_to_game_events(outcome.rolls)

            results.append(
                PlayerActionOutcome(
                    player_name=char_name,
                    outcome_description=outcome.description,
                    game_events=game_events
                )
            )

        return results

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

                case DiceRoll(character_name=name, statistic=stat):
                    engine_stat = self._map_stat_type(stat)
                    game_events.append(DiceEvent(player_name=name, statistic=engine_stat))

                case _:
                    raise ValueError(f"Unknown event type: {type(event)}")

        return game_events

    def _map_stat_type(self, llm_stat: StatisticType) -> StatType | None:
        if llm_stat == StatisticType.NO_STATISTIC:
            return None

        try:
            return StatType[llm_stat.name]
        except KeyError:
            return None
