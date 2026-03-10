import logging

from logic.brain.game_master_brain import GameMasterBrain
from logic.brain.player_action_outcome import PlayerActionOutcome
from logic.game.character import PlayerCharacter
from logic.game.game import Game
from logic.game.game_event import DiceEvent, GameEvent
from logic.game.player_action import PlayerAction
from logic.game.player_input import PlayerDiceRollResponse, PlayerDiceRollRequest, PlayerInputResponse, \
    PlayerInputRequest
from logic.game.scene import Scene, PlayerActionSequence


class GameMaster:
    def __init__(self):
        self._game: Game = None
        self._story: list[Scene] = []
        self._brain = GameMasterBrain()
        # The single source of truth for the current turn
        self._active_action: PlayerAction | None = None

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

    def _begin_new_scene(self):
        """
        helper function for start_next_scene
        """
        self._story.append(Scene())

    def start_next_scene(self) -> PlayerInputRequest:
        """
        Begins a new scene, executes initial events, and asks the player for intent.
        """
        state = self._game.capture_game_state()
        scene_setting, events = self._brain.provide_scene_setting(self._story, state)

        # 1. Initialize Scene
        self._story.append(Scene())
        self.current_scene.add(scene_setting)

        # 2. Execute Environmental/NPC events
        engine_sequences = self._game.execute_events(events)
        self.current_scene.extend(engine_sequences)

        # 3. Setup the turn-level Action object
        player_char = self._game.player_characters[0]
        self._active_action = PlayerAction(player_char.name)

        return PlayerInputRequest(player_char.name, "What do you do?")

    def handle_player_input(self, response: PlayerInputResponse) -> PlayerDiceRollRequest | None:
        """
        Entry point for text intent.
        """
        self._active_action.add_player_action(response.player_action)
        return self._orchestrate_turn()

    def handle_dice_result(self, result: PlayerDiceRollResponse) -> PlayerDiceRollRequest | None:
        """
        Entry point for dice results.
        """
        self._active_action.add_result_to_dice_roll(result.dice_result)
        return self._orchestrate_turn()

    def _orchestrate_turn(self) -> PlayerDiceRollRequest | None:
        """
        The core loop: Passes state to the brain and reacts to the returned events.
        """
        # Brain processes: Outcome Description -> Decider -> (Roll or Finalize)
        events = self._brain.process_player_action_outcome(
            self._story,
            self._active_action,
            self._game.capture_game_state()
        )

        # 1. Handle Dice Requests
        dice_event = next((e for e in events if isinstance(e, DiceEvent)), None)
        if dice_event:
            return PlayerDiceRollRequest(dice_event.player_name, dice_event.statistic)

        # 2. Handle Finalization
        if self._active_action.is_finished:
            self._record_final_narrative()
            return None

        return None

    def _record_final_narrative(self):
        """Logs and appends the final result to the scene."""
        summary = self._active_action.result_description

        # Add to story structure
        self.current_scene.add(PlayerActionSequence(
            player_name=self._active_action.player_name,
            content=summary
        ))

        # Output the turn summary to logs
        logging.info("--- TURN RESOLVED ---")
        logging.info(f"ACTION: {self._active_action.player_action}")
        logging.info(f"RESULT: {summary}")
        logging.info(f"SCENE TOTAL LINES: {len(self.current_scene.scene_sequences)}")
        logging.info("---------------------")
