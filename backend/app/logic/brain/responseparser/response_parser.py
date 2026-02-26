from abc import ABC, abstractmethod

from logic.brain.modelmanager.configured.models import StoryUpdate, ActionReaction
from logic.game.game_event import GameEvent
from logic.game.scene import SceneDescriptionSequence, ActionDescriptionSequence


class ResponseParser(ABC):
    @abstractmethod
    def parse_to_scene_setting(self, story_update: StoryUpdate) -> tuple[SceneDescriptionSequence, list[GameEvent]]:
        pass

    @abstractmethod
    def parse_to_action_reaction(self, action_reaction: ActionReaction) -> tuple[ActionDescriptionSequence, list[GameEvent]]:
        pass