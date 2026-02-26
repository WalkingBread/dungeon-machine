from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class SceneSequence(ABC):
    content: str

    @abstractmethod
    def get_type(self) -> str:
        """Return the type of the sequence."""
        pass

    def format_sequence(self) -> str:
        """Returns the labeled version: <type>: <content>"""
        return f"{self.get_type()}: {self.content}"


@dataclass
class GameIntroductionSequence(SceneSequence):
    def get_type(self) -> str:
        return "GameIntroduction"

@dataclass
class UserInputSequence(SceneSequence):
    def get_type(self) -> str:
        return "UserInput"

@dataclass
class SceneDescriptionSequence(SceneSequence):
    def get_type(self) -> str:
        return "SceneDescription"

@dataclass
class ActionDescriptionSequence(SceneSequence):
    def get_type(self) -> str:
        return "ActionDescription"

@dataclass
class EngineEventSequence(SceneSequence):
    def get_type(self) -> str:
        return "EngineEvent"

@dataclass
class Scene:
    scene_sequences: list[SceneSequence] = field(default_factory=list)

    def add(self, sequence: SceneSequence):
        self.scene_sequences.append(sequence)

    def get_scene_content(self) -> str:
        """Joins all sequences into a single formatted string."""
        return "\n".join(seq.format_sequence() for seq in self.scene_sequences)

    def __iter__(self):
        return iter(self.scene_sequences)