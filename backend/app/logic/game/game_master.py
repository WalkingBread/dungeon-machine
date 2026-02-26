from logic.brain.game_master_brain import GameMasterBrain
from logic.game.characters import PlayerManagedCharacter
from logic.game.game import Game
from logic.game.scene import Scene, UserInputSequence


class GameMaster:
    def __init__(self):
        self._game: Game = None
        self._history: list[Scene] = []
        self.current_scene: Scene = None
        self.brain = GameMasterBrain()

    @property
    def game(self):
        return self._game

    def create_game(self, theme: str, players: list[PlayerManagedCharacter]):
        self._game = Game(theme, players)

    def introduce_story(self):
        self.current_scene = Scene()
        self.current_scene.add(self.brain.get_game_introduction())

    def start_next_scene(self) -> Scene:
        scene_description_sequence, events = (
            self.brain.provide_scene_setting(self._history + [self.current_scene], self._game.capture_game_state()))
        self._begin_new_scene()
        self.current_scene.add(scene_description_sequence)
        engine_event_sequences = self._game.execute_events(events)
        for seq in engine_event_sequences: self.current_scene.add(seq)
        return self.current_scene

    def _begin_new_scene(self) -> Scene:
        """
        helper function for start_next_scene
        """
        self._history.append(self.current_scene)
        self.current_scene = Scene()

    def provide_action_reaction(self) -> Scene:
        action_outcome_description, events = (
            self.brain.provide_player_action_outcome(self._history + [self.current_scene], self._game.capture_game_state()))
        self.current_scene.add(action_outcome_description)
        engine_event_sequences = self._game.execute_events(events)
        for seq in engine_event_sequences: self.current_scene.add(seq)
        return self.current_scene

    def add_user_input(self, user_input: str) -> Scene:
        self.current_scene.add(UserInputSequence(user_input))
        return self.current_scene

    def _end_current_scene(self):
        self._history.append(self.current_scene)
        self.current_scene = None
