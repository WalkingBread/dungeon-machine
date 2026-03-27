import logging
import pytest

from logic.brain import GameMasterBrain
from logic.character import Character
from logic.game.player_action import PlayerAction
from logic.game.scene import Scene, GameIntroductionSequence
from logic.game.game import GameState
from logic.character.stat import StatType
from logic.dice import TestRollOutcome

@pytest.mark.llm
def test_provide_required_roll():
    brain = GameMasterBrain()

    character = Character.generate_character("Valerius")
    game_state = GameState(theme="", player_characters=[character], npc_characters=[])

    story = [Scene()]
    story[0].add(GameIntroductionSequence("A massive, rusted iron door blocks the path. It looks incredibly heavy."))

    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I want to use my brute strength to force the iron door open.")

    try:
        decision = brain.does_the_action_continue(story, action, game_state)
        logging.info(f"Does the action continue: {decision}")
        assert decision is True

        roll_request = brain.provide_required_roll(story, action, game_state)
        logging.info(f"Requested Stat: {roll_request.requested_stat}")
        logging.info(f"Intro Description: {roll_request.attempt_desc}")

        assert roll_request.requested_stat == StatType.STRENGTH
        assert len(roll_request.attempt_desc) > 0

    except Exception as e:
        logging.error(f"INTEGRATION CRASHED: {str(e)}", exc_info=True)
        raise e


@pytest.mark.llm
def test_provide_final_action_outcome():
    brain = GameMasterBrain()

    character = Character.generate_character("Valerius")
    game_state = GameState(theme="High Fantasy", player_characters=[character], npc_characters=[])

    story = [Scene()]
    story[0].add(GameIntroductionSequence("The corridor is patrolled by a single, bored-looking guard."))

    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I try to sneak past the guard while his back is turned.")

    action.add_new_dice_roll(StatType.AGILITY, "Moving from shadow to shadow.")
    action.add_result_to_dice_roll(TestRollOutcome.SUCCESS)

    logging.info(f"PRE-PROCESS STATE: {action.state}")

    try:
        desc = brain.provide_roll_outcome_desc(story, action, game_state)
        action.add_roll_description(desc)

        decision = brain.does_the_action_continue(story, action, game_state)
        assert decision is False

        final_outcome = brain.provide_final_action_outcome(story, action, game_state)

        logging.info("--- INTEGRATION RESULTS ---")
        logging.info(f"Final description: {final_outcome.outcome_desc}")
        logging.info(f"Game events: {final_outcome.game_events}")

        assert final_outcome is not None
        assert final_outcome.outcome_desc is not None
        assert len(final_outcome.outcome_desc) > 0

    except Exception as e:
        logging.error(f"INTEGRATION CRASHED: {str(e)}", exc_info=True)
        raise e
