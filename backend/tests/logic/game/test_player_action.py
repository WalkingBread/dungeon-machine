import pytest

from logic.character.stat import StatType
from logic.dice import TestRollOutcome
from logic.game.player_action import PlayerAction, PlayerActionState, DiceRollActionState, ActionVerificationException


def test_full_player_action_lifecycle():
    action = PlayerAction(player_name="Valerius")
    assert action.state == PlayerActionState.REQUIRES_PLAYER_INPUT

    action.add_player_action("I try to kick down the heavy oak door.")
    assert action.state == PlayerActionState.REQUIRES_DESCRIPTION
    assert action.player_action == "I try to kick down the heavy oak door."

    action.add_new_dice_roll(statistic=StatType.STRENGTH, attempt_desc="A powerful front kick.")
    assert action.state == PlayerActionState.REQUIRES_PLAYER_DICE_ROLL
    assert len(action.dice_rolls) == 1
    assert action.last_dice_roll.state == DiceRollActionState.REQUIRES_PLAYER

    outcome = TestRollOutcome.SUCCESS
    action.add_result_to_dice_roll(outcome)
    assert action.state == PlayerActionState.REQUIRES_DESCRIPTION
    assert action.last_dice_roll.dice_result == outcome
    assert action.last_dice_roll.state == DiceRollActionState.REQUIRES_DESCRIPTION

    action.add_roll_description("The wood splinters as your boot connects.")
    assert action.last_dice_roll.state == DiceRollActionState.FINISHED

    action.add_final_description("The door flies open, hitting the stone wall with a bang.")
    assert action.state == PlayerActionState.FINISHED
    assert action.is_finished is True


def test_cannot_add_action_twice():
    action = PlayerAction(player_name="Valerius")
    action.add_player_action("First action")

    with pytest.raises(ActionVerificationException, match="Invalid state"):
        action.add_player_action("Second action")


def test_cannot_add_roll_before_action():
    action = PlayerAction(player_name="Valerius")
    with pytest.raises(ActionVerificationException, match="Invalid state"):
        action.add_new_dice_roll(StatType.AGILITY)


def test_cannot_start_new_roll_while_one_is_active():
    action = PlayerAction(player_name="Valerius")
    action.add_player_action("Sneaking past guards")
    action.add_new_dice_roll(StatType.AGILITY)

    with pytest.raises(ActionVerificationException, match="Invalid state"):
        action.add_new_dice_roll(StatType.AGILITY)


def test_require_dice_rolls_decorator():
    action = PlayerAction(player_name="Valerius")
    action.add_player_action("Jump")
    action.state = PlayerActionState.REQUIRES_PLAYER_DICE_ROLL

    with pytest.raises(ActionVerificationException, match="requires at least one dice roll"):
        action.add_result_to_dice_roll(TestRollOutcome.EXTREME_SUCCESS)