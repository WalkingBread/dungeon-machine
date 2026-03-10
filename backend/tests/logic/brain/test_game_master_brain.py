import logging
import pytest

from logic.brain.game_master_brain import GameMasterBrain
from logic.character import Character
from logic.game.game_event import DiceEvent
from logic.game.player_action import PlayerAction, PlayerActionState
from logic.game.scene import Scene, GameIntroductionSequence
from logic.game.game import GameState
from logic.character.stat import StatType
from logic.dice import TestRollOutcome


# We assume your Brain class is defined and imported here
# from logic.brain.gm_brain import GameMasterBrain

@pytest.mark.llm
def test_process_player_action_outcome_integration():
    logging.info("=== STARTING REAL INTEGRATION TEST ===")

    brain = GameMasterBrain()

    character = Character.generate_character("Valerius")
    game_state = GameState(theme="", player_characters=[character], npc_characters=[])

    story = [Scene()]
    story[0].add(GameIntroductionSequence("The corridor is patrolled by a single, bored-looking guard."))

    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I try to sneak past the guard while his back is turned.")

    action.add_new_dice_roll(StatType.AGILITY, "Moving from shadow to shadow.")
    action.add_result_to_dice_roll(TestRollOutcome.SUCCESS)

    logging.info(f"PRE-PROCESS STATE: {action.state} | ROLL STATE: {action.last_dice_roll.state}")

    try:
        events = brain.process_player_action_outcome(story, action, game_state)

        logging.info("--- INTEGRATION TEST RESULTS ---")
        logging.info(f"Action State After Process: {action.state}")
        logging.info(f"Last Roll Narrative: {action.last_dice_roll.result_description}")
        logging.info(f"Final Action Description: {action.result_description}")
        logging.info(f"Emitted Events: {events}")

        if action.state == PlayerActionState.FINISHED:
            assert action.result_description is not None
            assert len(action.result_description) > 0
        else:
            assert len(action.dice_rolls) >= 1
            logging.info(f"Next Step Required: {action.dice_rolls[-1].statistic}")

    except Exception as e:
        logging.error(f"INTEGRATION CRASHED: {str(e)}", exc_info=True)
        raise e


@pytest.mark.llm
def test_integration_intent_to_roll_request():
    logging.info("=== TEST: INITIAL INTENT -> ROLL REQUEST ===")
    brain = GameMasterBrain()

    character = Character.generate_character("Valerius")
    game_state = GameState(theme="High Fantasy", player_characters=[character], npc_characters=[])

    story = [Scene()]
    story[0].add(GameIntroductionSequence("A massive, rusted iron door blocks the path. It looks incredibly heavy."))

    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I want to use my brute strength to force the iron door open.")

    logging.info(f"PRE-PROCESS STATE: {action.state}")

    events = brain.process_player_action_outcome(story, action, game_state)

    logging.info("--- INTEGRATION RESULTS ---")
    logging.info(f"Action State: {action.state}")

    if action.state == PlayerActionState.REQUIRES_PLAYER_DICE_ROLL:
        last_roll = action.last_dice_roll
        logging.info(f"Requested Stat: {last_roll.statistic}")
        logging.info(f"Intro Description: {last_roll.attempt_description}")
        logging.info(f"Events: {events}")

    assert action.state == PlayerActionState.REQUIRES_PLAYER_DICE_ROLL
    assert len(action.dice_rolls) == 1
    assert action.last_dice_roll.statistic == StatType.STRENGTH
    assert any(isinstance(e, DiceEvent) for e in events)