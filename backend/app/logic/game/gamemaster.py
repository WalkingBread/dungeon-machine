from logic.brain.dto.brain import SceneIntroductionDto, ActionStateDto
from logic.brain import GameMasterBrain
from logic.game.character import PlayerCharacter
from logic.game.game import Game
from logic.game.event import GameEvent
from logic.game.model.gamemaster import (
    DiceRollResponse, 
    DiceRollRequest, 
    PlayerInputResponse,
    PlayerInputRequest,
    GameIntroduction,
    SceneIntroduction,
    PlayerActionSegment
)
from logic.game.scene import (
    Scene, 
    PlayerActionSequence, 
    PlayerActionConsequenceSequence,
    DiceRollSequence,
    DiceRollConsequenceSequence,
    GameIntroductionSequence, 
    SceneDescriptionSequence
)

from functools import wraps

class GameNotStartedError(Exception):
    def __init__(self):
        super().__init__('Game must be created to perform this action.')

class ActionNotExpectedError(Exception):
    def __init__(self, expected_type, player):
        super().__init__(f"Game Master is not expecting a {expected_type} from {player}.")

def in_game(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.game:
            raise GameNotStartedError()
        return func(self, *args, **kwargs)
    return wrapper

def expect_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        game_master_response = func(self, *args, **kwargs)

        if isinstance(game_master_response, PlayerActionSegment):
            self._expected_player_action = game_master_response.request
            return game_master_response
        
        raise ValueError(f'{func.__name__} must return PlayerActionSegment to use this decorator.')

    return wrapper

def expected_action(expected_type):
    def decorator(func):
        @wraps(func)
        def wrapper(self, response_dto, *args, **kwargs):
            is_correct_type = isinstance(self._expected_player_action, expected_type)
        
            is_correct_player = False
            if self._expected_player_action:
                is_correct_player = self._expected_player_action.player_name == response_dto.player_name

            if not (is_correct_type and is_correct_player):
                raise ActionNotExpectedError(
                    expected_type.__name__,
                    response_dto.player_name
                )
                
            return func(self, response_dto, *args, **kwargs)
        return wrapper
    return decorator


class GameMaster:
    def __init__(self):
        self._game: Game | None = None
        self._story: list[Scene] = []
        self._brain = GameMasterBrain()
        self._expected_player_action = None

    @property
    def game(self):
        return self._game

    @property
    def story(self):
        return self._story

    @property
    def current_scene(self):
        return self._story[-1] if self._story else None
    
    @property
    def expects_action(self) -> bool:
        return self._expected_player_action is not None

    def create_game(self, theme: str, players: list[PlayerCharacter]):
        self._game = Game(theme, players)

    @in_game
    @expect_action
    def next_player_turn(self) -> PlayerActionSegment:
        return PlayerActionSegment()

    @in_game
    def get_introduction(self) -> GameIntroduction:
        self._init_scene()

        introduction: str = self._brain.provide_game_introduction(self.game.theme)
        self.current_scene.add(GameIntroductionSequence(introduction))

        return GameIntroduction(narrative=introduction)

    @in_game
    @expect_action
    def start_next_scene(self) -> PlayerActionSegment:
        state = self._game.capture_game_state()
        scene_introduction: SceneIntroductionDto = self._brain.provide_scene_intro(self._story, state)

        self._begin_new_scene(scene_introduction)

        player_char = self._game.player_characters[0]

        return PlayerActionSegment(
            narrative=scene_introduction.scene_intro,
            request=PlayerInputRequest(player_char.name, "What do you do?")
        )
    
    @in_game
    @expected_action(PlayerInputRequest)
    def handle_player_input(self, player_input: PlayerInputResponse) -> PlayerActionSegment:
        player_name = player_input.player_name

        self.current_scene.add(PlayerActionSequence(
            player_input.player_action,
            player_name
        ))

        action_state = self._get_action_state()

        self.current_scene.add(PlayerActionConsequenceSequence(
            action_state.narrative,
            player_name
        ))
        
        return self._continue_action(player_name, action_state)

    @in_game
    @expected_action(DiceRollRequest)
    def handle_dice_roll(self, dice_roll: DiceRollResponse) -> PlayerActionSegment:
        player_character = self._game.get_player_character(dice_roll.player_name)

        test_stat = self._expected_player_action.statistic
        test_outcome = player_character.stat_test(dice_roll.roll_value, test_stat)

        self.current_scene.add(DiceRollSequence(
            str(test_outcome),
            player_character.name
        ))

        action_state = self._get_roll_outcome()

        self.current_scene.add(DiceRollConsequenceSequence(
            action_state.narrative,
            player_character.name
        ))

        return self._continue_action(dice_roll.player_name, action_state)

    @in_game
    @expect_action
    def _continue_action(self, player_name: str, action_state: ActionStateDto) -> PlayerActionSegment:
        self._execute_events(action_state.game_events)

        match action_state.state:
            case 'INPUT':
                request = PlayerInputRequest(player_name, 'Your answer: ')
            case 'ROLL':
                roll_req = self._get_required_roll()
                request = DiceRollRequest(player_name, roll_req.requested_stat)
            case _:
                request = None

        return PlayerActionSegment(action_state.narrative, request)
    
    @in_game
    def _execute_events(self, game_events: list[GameEvent]) -> None:
        event_sequences = self._game.execute_events(game_events)
        self.current_scene.extend(event_sequences)

    def _get_action_state(self) -> ActionStateDto:
        return self._brain.provide_action_state(
            self._story, 
            self._game.capture_game_state()
        )

    def _get_required_roll(self):
        return self._brain.provide_required_roll(
            self._story, 
            self._game.capture_game_state()
        )

    def _get_roll_outcome(self) -> ActionStateDto:
        return self._brain.provide_roll_outcome_desc(
            self._story, 
            self._game.capture_game_state()
        )

    def _get_final_outcome(self):
        return self._brain.provide_final_action_outcome(
            self._story, 
            self._game.capture_game_state()
        )
    
    def _init_scene(self):
        self._story.append(Scene())

    def _begin_new_scene(self, scene_introduction: SceneIntroductionDto):
        self._init_scene()
        self.current_scene.add(SceneDescriptionSequence(scene_introduction.scene_intro))
        self._execute_events(scene_introduction.game_events)