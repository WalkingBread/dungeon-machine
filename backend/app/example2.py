from logic.character import Character
from logic.game.game_master import GameMaster

players = [Character.generate_character('Adam')]

gm = GameMaster()
gm.create_game("", players)
gm.introduce_story()

# init done

gm.start_next_scene()
gm.handle_player_action(players[0], "I am shouting like crazy to rise the attention of the nearby people!")

for scene in gm.story:
    print(scene.get_scene_content())

print("i use this as debugging breakpoint :)")