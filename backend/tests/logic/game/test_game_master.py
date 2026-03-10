import logging
import pytest
from logic.game.game_master import GameMaster
from logic.game.player_input import PlayerInputResponse, PlayerDiceRollResponse
from logic.dice import TestRollOutcome


@pytest.mark.llm
def test_gamemaster_full_turn_integration():
    logging.info("=== STARTING GAMEMASTER INTEGRATION TEST ===")

    # 1. Setup the GM and the Session State
    gm = GameMaster()

    # Generate a character through your existing logic
    # (Assuming Character.generate_character or similar exists)
    from logic.game.character import Character
    pc = Character.generate_character("Duncan")

    gm.create_game(theme="Grim Medieval", players=[pc])
    gm.introduce_story()

    # 2. Step 1: Start the Scene (Should return a text request)
    input_request = gm.start_next_scene()
    logging.info(f"GM Request: {input_request.player_action}")
    assert input_request.player_name == "Duncan"

    # 3. Step 2: Handle Player Intent
    # Scenario: Duncan tries to break a rusted gate.
    user_input = PlayerInputResponse(
        player_name="Duncan",
        player_action="I throw my shoulder against the rusted iron gate to force it open."
    )

    dice_request = gm.handle_player_input(user_input)

    # The LLM should recognize this needs a STRENGTH check
    assert dice_request is not None
    logging.info(f"GM Decision: Needs a {dice_request.statistic.name} roll.")

    # 4. Step 3: Handle Dice Result
    # We simulate a successful roll
    dice_result = PlayerDiceRollResponse(
        player_name="Duncan",
        dice_result=TestRollOutcome.SUCCESS
    )

    final_result = gm.handle_dice_result(dice_result)

    # Since it's a success on a simple gate, it should finish the action
    assert final_result is None

    # 5. Step 4: Verify Scene Integration
    # The result_description from the LLM should now be in the scene history
    scene_content = gm.current_scene.get_scene_content()

    logging.info("--- FINAL SCENE CONTENT ---")
    logging.info(scene_content)
    logging.info("---------------------------")

    assert "Duncan" in scene_content
    # Check if the LLM actually wrote a story (not just empty)
    assert len(scene_content) > 100