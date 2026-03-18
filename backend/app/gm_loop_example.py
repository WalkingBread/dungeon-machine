from logic.game.game_master import GameMaster
from logic.game.character import Character
from logic.dice import TestRollOutcome
from logic.game.game_master_dtos import PlayerInputResponse, PlayerDiceRollResponse

import warnings

# This MUST be at the top of the file
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")
warnings.filterwarnings("ignore", message="PydanticSerializationUnexpectedValue.*")


def get_dice_roll() -> tuple[int, TestRollOutcome]:
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

    return roll, outcome


def game_loop_example():
    gm = GameMaster()
    player = Character.generate_character("Duncan")
    gm.create_game(theme="Dark Fantasy", players=[player])

    intro = gm.get_introduction()
    print(f"[GM] Introduction:\n{intro.text}\n")

    while True:
        scene_narrative, input_request = gm.start_next_scene()
        print(f"[GM] Current Scene:\n {scene_narrative.text}")

        player_intent = input(f"[GM]: {input_request.player_name} - {input_request.text}\nInput: ")
        input_response = PlayerInputResponse(
            player_name=player.name,
            player_action=player_intent
        )

        action_generator = gm.handle_player_input(input_response)

        try:
            step_narrative, dice_request = next(action_generator)

            while True:
                print(f"\n[GM]: {step_narrative.text}")

                if dice_request:

                    print(f"[Roll Required: {dice_request.statistic}]")
                    input(">>> Press [ENTER] to roll...")
                    roll, outcome = get_dice_roll()
                    print(f"[DICE] You rolled a {roll}! Outcome: {outcome.name}")

                    dice_response = PlayerDiceRollResponse(
                        player_name=player.name,
                        dice_result=outcome
                    )
                    step_narrative, dice_request = action_generator.send(dice_response)

                else:
                    input("...Press Enter to continue...")
                    step_narrative, dice_request = next(action_generator)

        except StopIteration:
            print("\n--- Action Resolved. Moving to the next scene... Press Ctrl+C to stop---\n")


if __name__ == "__main__":
    game_loop_example()