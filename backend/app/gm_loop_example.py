from logic.game.gamemaster import GameMaster
from logic.game.character import Character
from logic.dice.type import DiceType
from logic.game.dto.gamemaster import PlayerInputResponse, PlayerDiceRollResponse, PlayerDiceRollRequest
from services.dice.dice import DiceService

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")
warnings.filterwarnings("ignore", message="PydanticSerializationUnexpectedValue.*")


def game_loop_example():
    dice_service = DiceService()

    gm = GameMaster()
    player = Character.generate_character("Duncan")
    gm.create_game(theme="Star Wars", players=[player])

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

        narrative_segment, roll_request = gm.handle_player_input(input_response)
        print(f"\n[GM]: {narrative_segment.text}")

        while roll_request:
            print(f"[Roll Required For: {roll_request.statistic}]")
            input(">>> Press [ENTER] to roll...")
            roll_value = dice_service.roll_dice(DiceType.D100)
            dice_roll_response = PlayerDiceRollResponse(player.name, roll_value)

            narrative_segment = gm.handle_dice_roll(dice_roll_response)
            print(f"\n[GM]: {narrative_segment.text}")

            narrative_segment, roll_request = gm.continue_action()
            print(f"\n[GM]: {narrative_segment.text}")


if __name__ == "__main__":
    game_loop_example()