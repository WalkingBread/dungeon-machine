from typing import Generator

from logic.brain.dto.brain import SceneIntroductionDto
from logic.brain import GameMasterBrain
from logic.game.character import PlayerCharacter
from logic.game.game import Game
from logic.game.player_action import PlayerAction
from logic.game.dto.gamemaster import (
    PlayerDiceRollResponse, 
    PlayerDiceRollRequest, 
    PlayerInputResponse,
    PlayerInputRequest,
    NarrativeSegment
)
from logic.game.scene import (
    Scene, 
    PlayerActionSequence, 
    GameIntroductionSequence, 
    SceneDescriptionSequence
)

class GameMaster:
    def __init__(self):
        self._game: Game | None = None
        self._story: list[Scene] = []
        self._brain = GameMasterBrain()
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

    def get_introduction(self) -> NarrativeSegment:
        if self._game is None:
            raise Exception("You need to start the game first!")

        self._begin_new_scene()

        intro: str = self._brain.provide_game_introduction(self.game.theme)
        self.current_scene.add(GameIntroductionSequence(intro))

        return NarrativeSegment(intro)


    def start_next_scene(self) -> tuple[NarrativeSegment, PlayerInputRequest]:
        state = self._game.capture_game_state()
        scene_intro: SceneIntroductionDto = self._brain.provide_scene_intro(self._story, state)

        self._begin_new_scene()
        self.current_scene.add(SceneDescriptionSequence(scene_intro.scene_intro))

        engine_sequences = self._game.execute_events(scene_intro.game_events)
        self.current_scene.extend(engine_sequences)

        player_char = self._game.player_characters[0]
        self._active_action = PlayerAction(player_char.name)

        return NarrativeSegment(scene_intro.scene_intro), PlayerInputRequest(player_char.name, "What do you do?")
    

    def handle_player_input(self, player_input: PlayerInputResponse):
        self._active_action.add_player_action(player_input.player_action)
        return self.continue_action()

    
    def handle_dice_roll(self, player_dice_roll: PlayerDiceRollResponse):
        player_character = self._game.get_player_character(player_dice_roll.player_name)

        test_stat = self._active_action.last_dice_roll.statistic

        test_outcome = player_character.stat_test(player_dice_roll.roll_value, test_stat)
        self._active_action.add_result_to_dice_roll(test_outcome)

        outcome_desc = self._get_roll_outcome()
        self._active_action.add_roll_description(outcome_desc)

        return NarrativeSegment(outcome_desc)


    def continue_action(self):
        if self._should_action_continue():
            roll_req_dto = self._get_required_roll()
            self._active_action.add_new_dice_roll(roll_req_dto.requested_stat, roll_req_dto.attempt_desc)

            segment = NarrativeSegment(roll_req_dto.attempt_desc)
            roll_request = PlayerDiceRollRequest(self._active_action.player_name, roll_req_dto.requested_stat)

            return segment, roll_request
        
        return self.resolve_action(), None


    def resolve_action(self):
        final_outcome = self._get_final_outcome()

        self._active_action.add_final_description(final_outcome.outcome_desc)

        self.current_scene.add(PlayerActionSequence(
            self._active_action.player_name,
            final_outcome.outcome_desc
        ))

        event_sequences = self._game.execute_events(final_outcome.game_events)
        self.current_scene.extend(event_sequences)

        return NarrativeSegment(final_outcome.outcome_desc)


    def _should_action_continue(self) -> bool:
        return self._brain.does_the_action_continue(
            self._story, 
            self._active_action, 
            self._game.capture_game_state()
        )

    def _get_required_roll(self):
        return self._brain.provide_required_roll(
            self._story, 
            self._active_action, 
            self._game.capture_game_state()
        )

    def _get_roll_outcome(self) -> str:
        return self._brain.provide_roll_outcome_desc(
            self._story, 
            self._active_action, 
            self._game.capture_game_state()
        )

    def _get_final_outcome(self):
        return self._brain.provide_final_action_outcome(
            self._story, 
            self._active_action, 
            self._game.capture_game_state()
        )

    def _begin_new_scene(self):
        self._story.append(Scene())
