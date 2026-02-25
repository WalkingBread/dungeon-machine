from dataclasses import dataclass
from logic.game.state import GameState
from logic.game.sequence import StorySequence

@dataclass
class GameContext:
    game_state: GameState
    last_sequence: StorySequence

    def to_dict(self):
        return {
            'current_game_state': self.game_state.to_dict(),
            'last_story_part': self.last_sequence.to_dict()
        }