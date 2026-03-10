import logging
import sys
import time
from logic.game.game_master import GameMaster
from logic.game.character import Character
from logic.dice import TestRollOutcome
from logic.game.player_input import PlayerInputResponse, PlayerDiceRollResponse

import warnings
import logging

# This MUST be at the top of the file
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")
warnings.filterwarnings("ignore", message="PydanticSerializationUnexpectedValue.*")


def get_dice_roll(player_name, statistic):
    print(f"\n[SYSTEM] {player_name} needs to roll for {statistic.name}...")
    input(">>> Press [ENTER] to roll...")

    import random
    roll = random.randint(1, 20)

    if roll == 20:
        outcome = TestRollOutcome.EXTREME_SUCCESS
    elif roll >= 12:
        outcome = TestRollOutcome.SUCCESS
    elif roll >= 5:
        outcome = TestRollOutcome.FAILURE
    else:
        outcome = TestRollOutcome.EXTREME_FAILURE

    print(f"[DICE] You rolled a {roll}! Outcome: {outcome.name}")
    return outcome


# --- 2. Manual Setup ---
gm = GameMaster()
duncan = Character.generate_character("Duncan")
gm.create_game(theme="Dark Fantasy", players=[duncan])

# --- 3. Start the Story ---
gm.introduce_story()

print("=" * 50)
print("\nINTRO\n")
print(gm.current_scene.get_scene_content())

active_req = gm.start_next_scene()

print(f"\n[GM]: {gm.current_scene.scene_sequences[0].content}")

# --- 4. The Loop ---
while active_req is not None:
    # A: Text Input Request
    if hasattr(active_req, 'player_action'):
        user_text = input(f"\n[{duncan.name}]: ")

        response = PlayerInputResponse(
            player_name=duncan.name,
            player_action=user_text
        )
        active_req = gm.handle_player_input(response)

    # B: Dice Roll Request
    elif hasattr(active_req, 'statistic'):
        result = get_dice_roll(duncan.name, active_req.statistic)

        dice_response = PlayerDiceRollResponse(
            player_name=duncan.name,
            dice_result=result
        )
        active_req = gm.handle_dice_result(dice_response)

print("\n" + "=" * 50)
print("SCENE RESOLVED")
print("=" * 50)
print(gm.current_scene.get_scene_content())