from logic.brain.modelmanager.request_structures import StoryUpdate, PlayerActionOutcome
from logic.game.game_event import GameEvent
from logic.game.scene import SceneDescriptionSequence, ActionDescriptionSequence


class ResponseParser:

    def parse_to_scene_setting(self, story_update: StoryUpdate) \
            -> tuple[SceneDescriptionSequence, list[GameEvent]]:

        sequence = SceneDescriptionSequence(content=story_update.new_story_segment)

        events = []
        for event in story_update.engine_events:
            events.append(GameEvent(event_str=str(event)))

        return sequence, events

    def parse_to_player_action_outcome(self, action_outcome: PlayerActionOutcome) \
            -> tuple[ActionDescriptionSequence, list[GameEvent]]:

        sequence = ActionDescriptionSequence(content=action_outcome.description)

        events = []
        for roll in action_outcome.rolls:
            events.append(GameEvent(event_str=str(roll)))

        return sequence, events
