from logic.game.session import SessionManager

session_manager = SessionManager()
session = session_manager.create_session()

player = session.join('pussydestroyer')
player_character = session.create_character(player, 'Ser Duncan The Tall')

game_master = session.game_master

started = session.start_game('medieval')
if started:
    game_master.introduce_story()
    game_master.start_next_scene()
    print(game_master.current_scene)
else:
    print('Not all players are ready.')