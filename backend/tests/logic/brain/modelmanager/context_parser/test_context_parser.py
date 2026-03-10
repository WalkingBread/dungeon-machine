import logging

import pytest

from logic.brain.contextparser.context_parser_impl import ContextParserImpl
from logic.character import Character
from logic.character.stat import StatType
from logic.dice import TestRollOutcome
from logic.game.character import GameCharacter, PlayerCharacter
from logic.game.game import GameState
from logic.game.player_action import PlayerAction, ActionVerificationException
from logic.game.scene import Scene, GameIntroductionSequence


def test_character_to_json():
    character: GameCharacter = Character.generate_character("Test Character")

    context_parser = ContextParserImpl()

    parsed = context_parser.parse_character_to_json(character)

    logging.info(f"Character: {character}\n\n")
    logging.info(f"Parsed character: {parsed}")

def test_parse_game_state():
    player_list = [Character.generate_character("Test Character"), Character.generate_character("Test Character2")]
    npc_list = [Character.generate_character("Game Char"), Character.generate_character("Game Char2")]

    game_state = GameState("", player_list, npc_list)

    context_parser = ContextParserImpl()

    parsed = context_parser.parse_game_state(game_state)

    logging.info(f"Character: {game_state}\n\n")
    logging.info(f"Parsed character: {parsed}")

def test_parse_action_history_step_by_step():
    """
    Detailed log of the action history at every transition point
    to verify state-string consistency.
    """
    logging.info("=== STARTING GRANULAR HISTORY LOG ===")
    context_parser = ContextParserImpl()
    action = PlayerAction(player_name="Kaelen")

    action.add_player_action("I try to sneak past the sleeping guard.")
    logging.info("--- [1] INTENT ONLY ---")
    logging.info(f"\n{context_parser.parse_action_history(action)}")

    action.add_new_dice_roll(StatType.LUCK, "Checking the floor for creaky boards.")
    logging.info("--- [2] FIRST ROLL: ATTEMPT DESC (NO RESULT) ---")
    logging.info(f"\n{context_parser.parse_action_history(action)}")

    action.add_result_to_dice_roll(TestRollOutcome.SUCCESS)
    action.add_roll_description("You spot a loose floorboard and navigate around it.")
    logging.info("--- [3] FIRST ROLL: COMPLETED ---")
    logging.info(f"\n{context_parser.parse_action_history(action)}")

    action.add_new_dice_roll(StatType.AGILITY, "Moving silently while the guard snores.")
    logging.info("--- [4] SECOND ROLL: ATTEMPT DESC (NO RESULT) ---")
    logging.info(f"\n{context_parser.parse_action_history(action)}")

    action.add_result_to_dice_roll(TestRollOutcome.EXTREME_SUCCESS)
    action.add_roll_description("You move like a shadow; the guard doesn't even stir.")
    logging.info("--- [5] SECOND ROLL: COMPLETED ---")
    logging.info(f"\n{context_parser.parse_action_history(action)}")

    action.add_final_description("You successfully reach the heavy iron door on the far side.")
    logging.info("--- [6] FINAL ACTION DESCRIPTION ---")
    logging.info(f"\n{context_parser.parse_action_history(action)}")

def test_parse_action_history_failure_path():
    """
    Logs how a failure looks in the history string.
    """
    action = PlayerAction(player_name="Thorg")
    action.add_player_action("I attempt to bash the stone golem with my hammer.")

    context_parser = ContextParserImpl()

    action.add_new_dice_roll(StatType.STRENGTH, "A massive overhead swing.")
    action.add_result_to_dice_roll(TestRollOutcome.EXTREME_FAILURE)
    action.add_roll_description("Your hammer strikes a glancing blow, vibrating painfully through your arms.")

    logging.info("--- FAILURE PATH LOG ---")
    logging.info(f"\n{context_parser.parse_action_history(action)}")


@pytest.fixture
def setup_game_data():
    """Fixture to provide basic game objects."""
    character: PlayerCharacter = Character.generate_character(name="Valerius")
    state = GameState(theme="", player_characters=[character], npc_characters=[])

    scene = Scene()
    scene.add(GameIntroductionSequence("You stand before the Iron Gate of Galdur."))

    return [scene], state


def test_parse_to_player_action_context_success(setup_game_data):
    story, game_state = setup_game_data
    parser = ContextParserImpl()

    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I try to pick the lock on the gate.")
    action.add_new_dice_roll(StatType.AGILITY, "Using high-quality lockpicks.")
    action.add_result_to_dice_roll(TestRollOutcome.SUCCESS)
    # Note: We stop here to see if the parser captures the unfinished second roll state

    # 2. Run the parser
    context = parser.parse_to_player_action_context(story, action, game_state)

    # 3. Log the results for visual verification
    logging.info("--- GENERATED LLM CONTEXT ---")
    for key, value in context.items():
        logging.info(f"KEY: {key}\nVALUE:\n{value}\n{'-' * 20}")

    # 4. Assertions
    assert context["scene"] == "GameIntroduction: You stand before the Iron Gate of Galdur."
    assert "Valerius" in context["game_state"]
    assert "wants to: I try to pick the lock" in context["intent"]
    assert "ROLL 1 (AGILITY)" in context["action_history"]
    assert "Result: SUCCESS" in context["action_history"]


def test_parse_to_player_action_context_validation_failure(setup_game_data):
    story, game_state = setup_game_data
    parser = ContextParserImpl()

    # Create an action but DON'T add an intent (too short)
    action = PlayerAction(player_name="Valerius")
    action.player_action = "no"  # Too short, should trigger decorator

    with pytest.raises(ActionVerificationException) as excinfo:
        parser.parse_to_player_action_context(story, action, game_state)

    assert "too short" in str(excinfo.value).lower()
    logging.info(f"Caught expected validation error: {excinfo.value}")


def test_parse_to_player_action_context_empty_history(setup_game_data):
    story, game_state = setup_game_data
    parser = ContextParserImpl()

    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I shout a challenge to the guards!")

    context = parser.parse_to_player_action_context(story, action, game_state)

    # History should be an empty string, not a "No history" message
    assert context["action_history"] == ""
    logging.info("Verified: Empty history handled correctly.")

