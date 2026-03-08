from app.logic.game.character import PlayerCharacter
from app.logic.game.game_master import GameMaster
from app.logic.game.player_input import PlayerInputRequest
from logic.game.session import SessionManager

session_manager = SessionManager()
session = session_manager.create_session()

player = session.join('pussydestroyer')
player_character: PlayerCharacter = session.create_character(player, 'Jason')

game_master: GameMaster = session.game_master

started = session.start_game('medieval')
if started:
    game_master.introduce_story()
    requests: list[PlayerInputRequest] = game_master.start_next_scene()
    print(game_master.current_scene)
    for request in requests:
        print(f"{request.player_name} - {request.player_action}")
    print(game_master.current_scene)
    action = input("what do you do?")
    response = PlayerInputRequest(player_character.name, action)
    responses = game_master.handle_new_actions([response])
    print(responses)
    print(game_master.current_scene)


else:
    print('Not all players are ready.')