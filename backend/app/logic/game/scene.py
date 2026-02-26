from dataclasses import dataclass, field
from abc import ABC

@dataclass
class SceneSequence(ABC):
    content: str

    @property
    def sequence_type(self) -> str:
        return self.__class__.__name__.removesuffix("Sequence")

    def format_sequence(self) -> str:
        """Returns the labeled version: <type>: <content>"""
        return f"{self.sequence_type}: {self.content}"


@dataclass
class GameIntroductionSequence(SceneSequence):
    pass

@dataclass
class UserInputSequence(SceneSequence): # will add additional fields like player_id later on
    pass

@dataclass
class SceneDescriptionSequence(SceneSequence):
    pass

@dataclass
class ActionDescriptionSequence(SceneSequence):
    pass

@dataclass
class EngineEventSequence(SceneSequence):
    pass

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