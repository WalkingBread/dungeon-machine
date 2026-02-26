from abc import ABC, abstractmethod

from logic.brain.modelmanager.configured.models import StoryUpdate, ActionReaction

class ModelManager(ABC):
    @abstractmethod
    def provide_scene_setting(self, model_context: dict) -> StoryUpdate:
        pass

    @abstractmethod
    def provide_action_reaction(self, model_context: dict) -> ActionReaction:
        pass