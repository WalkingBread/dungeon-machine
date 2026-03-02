from logic.brain.modelmanager.request_structures import StoryUpdate, PlayerActionOutcome
from logic.game.game_event import GameEvent
from logic.game.scene import SceneDescriptionSequence, ActionDescriptionSequence


class ResponseParser:

    def parse_to_scene_setting(self, story_update: StoryUpdate) \
            -> tuple[SceneDescriptionSequence, list[GameEvent]]:

        sequence = SceneDescriptionSequence(content=story_update.new_story_segment)
        events = self._map_to_game_events(story_update.engine_events)

        return sequence, events

    def parse_to_player_action_outcome(self, action_outcome: PlayerActionOutcome) \
            -> tuple[ActionDescriptionSequence, list[GameEvent]]:

        sequence = ActionDescriptionSequence(content=action_outcome.description)
        events = self._map_to_game_events(action_outcome.rolls)

        return sequence, events

    def _map_to_game_events(self, llm_events) -> list[GameEvent]:
        game_events = []
        for llm_event in llm_events:
            game_events.append(GameEvent(event_str=str(llm_event)))

        return game_events
