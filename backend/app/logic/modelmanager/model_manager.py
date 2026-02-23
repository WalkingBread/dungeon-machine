from abc import ABC, abstractmethod

class ModelManager(ABC):
    @abstractmethod
    def provide_scene_description(self, model_context: dict):
        pass

    @abstractmethod
    def provide_character_events(self, model_context: dict):
        pass