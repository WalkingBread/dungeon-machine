from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps

from logic.character.stat import StatType
from logic.dice import TestRollOutcome

class ActionVerificationException(Exception):
    """Base class for all player action errors."""
    pass

def require_state(state: PlayerActionState):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.state != state:
                raise ActionVerificationException(f"Invalid state: {self.state}. Expected: {state}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def check_action_text(null=True):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            exists = self.player_action is not None
            if null and exists:
                raise ActionVerificationException(
                    f"{func.__name__} requires player_action to be empty (null)."
                )
            if not null and not exists:
                raise ActionVerificationException(
                    f"{func.__name__} requires player_action to be set (not null)."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def require_dice_rolls(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.dice_rolls or len(self.dice_rolls) == 0:
            raise ActionVerificationException(
                f"{func.__name__} requires at least one dice roll to exist."
            )
        return func(self, *args, **kwargs)
    return wrapper


def require_last_roll_state(expected_roll_state: DiceRollActionState):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.dice_rolls:
                raise ActionVerificationException(
                    f"{func.__name__} failed: No dice rolls exist."
                )
            last_roll = self.dice_rolls[-1]
            if last_roll.state != expected_roll_state:
                raise ActionVerificationException(
                    f"{func.__name__} failed: Last dice roll is in state {last_roll.state}, "
                    f"but expected {expected_roll_state}."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def require_no_active_roll(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.dice_rolls:
            last_roll = self.dice_rolls[-1]
            if last_roll.state != DiceRollActionState.FINISHED:
                raise ActionVerificationException(
                    f"Cannot start new roll: Last roll is still in state {last_roll.state}"
                )
        return func(self, *args, **kwargs)
    return wrapper

class PlayerActionState(Enum):
    REQUIRES_PLAYER_INPUT = auto()
    REQUIRES_DESCRIPTION = auto()
    REQUIRES_PLAYER_DICE_ROLL = auto()
    FINISHED = auto()

class DiceRollActionState(Enum):
    REQUIRES_PLAYER = auto()
    REQUIRES_DESCRIPTION = auto()
    FINISHED = auto()

@dataclass
class PlayerAction:
    player_name: str
    player_action: str | None = None # this is action input used by the player
    state: PlayerActionState = PlayerActionState.REQUIRES_PLAYER_INPUT
    dice_rolls: list[DiceRollAction] = field(default_factory=list)
    result_description: str | None = None  # this is a final description of the full action with dice rolls and their outcomes

    @property
    def last_dice_roll(self) -> DiceRollAction | None:
        return self.dice_rolls[-1] if self.dice_rolls else None

    @property
    def is_finished(self) -> bool:
        return self.state == PlayerActionState.FINISHED

    @require_state(PlayerActionState.REQUIRES_PLAYER_INPUT)
    @check_action_text(null=True)
    def add_player_action(self, player_action: str):
        self.player_action = player_action
        self.state = PlayerActionState.REQUIRES_DESCRIPTION

    @require_state(PlayerActionState.REQUIRES_DESCRIPTION)
    @check_action_text(null=False)
    @require_no_active_roll
    def add_new_dice_roll(self, statistic: StatType | None):
        self.state = PlayerActionState.REQUIRES_PLAYER_DICE_ROLL
        new_dice_roll = DiceRollAction(self.player_name, statistic)
        self.dice_rolls.append(new_dice_roll)

    @require_state(PlayerActionState.REQUIRES_PLAYER_DICE_ROLL)
    @check_action_text(null=False)
    @require_dice_rolls
    @require_last_roll_state(DiceRollActionState.REQUIRES_PLAYER)
    def add_result_to_dice_roll(self, dice_result: TestRollOutcome):
        self.last_dice_roll.dice_result = dice_result
        self.last_dice_roll.state = DiceRollActionState.REQUIRES_DESCRIPTION
        self.state = PlayerActionState.REQUIRES_DESCRIPTION

    @require_state(PlayerActionState.REQUIRES_DESCRIPTION)
    @check_action_text(null=False)
    def add_roll_description(self, description: str):
        self.last_dice_roll.result_description = description
        self.last_dice_roll.state = DiceRollActionState.FINISHED

    @require_state(PlayerActionState.REQUIRES_DESCRIPTION)
    @check_action_text(null=False)
    @require_last_roll_state(DiceRollActionState.FINISHED)
    def add_final_description(self, description: str):
        self.result_description = description
        self.state = PlayerActionState.FINISHED


@dataclass
class DiceRollAction:
    player_name: str
    statistic: StatType | None = None
    state: DiceRollActionState = DiceRollActionState.REQUIRES_PLAYER
    dice_result: TestRollOutcome | None = None
    result_description: str | None = None # what happens after the dice is rolled :)