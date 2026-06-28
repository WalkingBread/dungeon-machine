from logic.brain.dto.brain import SceneIntroductionDto, ActionStateDto
from logic.brain import GameMasterBrain
from logic.game.character import PlayerCharacter
from logic.game.game import Game
from logic.game.player_action import PlayerAction
from logic.game.model.gamemaster import (
    DiceRollResponse, 
    DiceRollRequest, 
    PlayerInputResponse,
    PlayerInputRequest,
    GameIntroduction,
    SceneIntroduction,
    PlayerActionSegment,
    GameMasterResponse
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

    def get_introduction(self) -> GameIntroduction:
        if self._game is None:
            raise Exception("You need to start the game first!")

        self._begin_new_scene()

        introduction: str = self._brain.provide_game_introduction(self.game.theme)
        self.current_scene.add(GameIntroductionSequence(introduction))

        return GameIntroduction(narrative=introduction)


    def start_next_scene(self) -> SceneIntroduction:
        state = self._game.capture_game_state()
        scene_intro: SceneIntroductionDto = self._brain.provide_scene_intro(self._story, state)

        self._begin_new_scene()
        self.current_scene.add(SceneDescriptionSequence(scene_intro.scene_intro))

        engine_sequences = self._game.execute_events(scene_intro.game_events)
        self.current_scene.extend(engine_sequences)

        player_char = self._game.player_characters[0]
        self._active_action = PlayerAction(player_char.name)

        return SceneIntroduction(
            narrative=scene_intro.scene_intro,
            input_requests=[PlayerInputRequest(player_char.name, "What do you do?")]
        )
    

    def handle_player_input(self, player_input: PlayerInputResponse) -> PlayerActionSegment:
        self._active_action.add_player_action(player_input.player_action)

        action_state = self._get_action_state()
        
        return self._continue_action(action_state)

    
    def handle_dice_roll(self, player_dice_roll: DiceRollResponse) -> PlayerActionSegment:
        player_character = self._game.get_player_character(player_dice_roll.player_name)

        test_stat = self._active_action.last_dice_roll.statistic

        test_outcome = player_character.stat_test(player_dice_roll.roll_value, test_stat)
        self._active_action.add_result_to_dice_roll(test_outcome)

        action_state = self._get_action_state()
        self._active_action.add_roll_description(action_state.narrative)

        return self._continue_action(action_state)


    def _continue_action(self, action_state: ActionStateDto) -> PlayerActionSegment:
        player_name = self._active_action.player_name
        
        engine_sequences = self._game.execute_events(action_state.game_events)
        self.current_scene.extend(engine_sequences)

        if action_state.state == 'INPUT':
            self._resolve_action_segment()
            self._active_action = PlayerAction(player_name)

            return PlayerActionSegment(
                action_state.narrative,
                PlayerInputRequest(player_name, 'Your answer: ')
            )
        elif action_state.state == 'ROLL':
            roll_request = self._get_required_roll()
            self._active_action.add_new_dice_roll(roll_request.requested_stat, roll_request.attempt_desc)

            return PlayerActionSegment(
                action_state.narrative,
                DiceRollRequest(player_name, roll_request.requested_stat)
            )

        self._resolve_action_segment()

        return PlayerActionSegment(action_state.narrative)


    def _resolve_action_segment(self) -> None:
        final_outcome = self._get_final_outcome()

        self._active_action.add_final_description(final_outcome.desc)

        self.current_scene.add(PlayerActionSequence(
            final_outcome.desc,
            self._active_action.player_name
        ))


    def _get_action_state(self) -> ActionStateDto:
        return self._brain.provide_action_state(
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
