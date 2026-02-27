from logic.brain.game_master_brain import GameMasterBrain
from logic.game.character import PlayerCharacter
from logic.game.game import Game
from logic.game.scene import Scene, PlayerInputSequence


class GameMaster:
    def __init__(self):
        self._game: Game = None
        self._story: list[Scene] = []
        self._brain = GameMasterBrain()

    @property
    def game(self):
        return self._game

    @property
    def story(self):
        return self._story

    @property
    def current_scene(self):
        return self._story[-1] if self._story else None

    def create_game(self, theme: str, players: list[PlayerCharacter]):
        self._game = Game(theme, players)

    def introduce_story(self):
        self._begin_new_scene()
        self.current_scene.add(self._brain.get_game_introduction())

    def start_next_scene(self) -> Scene:
        scene_description_sequence, events = (
            self._brain.provide_scene_setting(self._story, self._game.capture_game_state()))
        self._begin_new_scene()
        self.current_scene.add(scene_description_sequence)
        engine_event_sequences = self._game.execute_events(events)
        for seq in engine_event_sequences: self.current_scene.add(seq)
        return self.current_scene

    def _begin_new_scene(self):
        """
        helper function for start_next_scene
        """
        self._story.append(Scene())

    def handle_player_action(self, player: PlayerCharacter, player_input: str) -> Scene:
        self.current_scene.add(
            PlayerInputSequence(
                player_id=player.character_id,
                player_name=player.name,
                content=player_input))
        self._process_player_action()
        return self.current_scene

    def _process_player_action(self):
        """
        a helper function for add_user_input, which processes the input,
        consults brain to describe and get events and calls engine to execute logic
        """
        action_outcome_description, events = (
            self._brain.provide_player_action_outcome(self._story, self._game.capture_game_state()))
        self.current_scene.add(action_outcome_description)
        engine_event_sequences = self._game.execute_events(events)
        for seq in engine_event_sequences: self.current_scene.add(seq)
