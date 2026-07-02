from logic.game.gamemaster import GameMaster
from logic.game.character import Character
from logic.dice.type import DiceType
from logic.game.model.gamemaster import PlayerInputResponse, PlayerInputRequest, DiceRollResponse, DiceRollRequest, PlayerActionSegment
from services.dice.dice import DiceService

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")
warnings.filterwarnings("ignore", message="PydanticSerializationUnexpectedValue.*")


def game_loop_example():
    dice_service = DiceService()

    gm = GameMaster()
    gm.create_game(theme="Call of Cthulu", players=[
        Character.generate_character("Duncan")
    ])

    intro = gm.get_introduction()
    print(f"[GM] Introduction:\n{intro.narrative}\n")

    while True:
        action_segment = gm.start_next_scene()

        while not gm.round_finished:
            print(f"[GM] Current Scene:\n {action_segment.narrative}")
            player = gm.current_player

            print(f'[GM]: {player.name}\'s turn.')

            while gm.expects_action:
                if isinstance(action_segment.request, DiceRollRequest):
                    print(f"[Roll Required For: {action_segment.request.statistic}]")
                    input(">>> Press [ENTER] to roll...")
                    roll_value = dice_service.roll_dice(DiceType.D100)
                    dice_roll_response = DiceRollResponse(player.name, roll_value)

                    action_segment = gm.handle_dice_roll(dice_roll_response)

                elif isinstance(action_segment.request, PlayerInputRequest):
                    player_intent = input(f"[GM]: {action_segment.request.player_name} - {action_segment.request.text}\nInput: ")
                    input_response = PlayerInputResponse(
                        player_name=player.name,
                        player_action=player_intent
                    )

                    action_segment = gm.handle_player_input(input_response)
                
                print(f"\n[GM]: {action_segment.narrative}")

            action_segment = gm.next_player_turn()


if __name__ == "__main__":
    game_loop_example()