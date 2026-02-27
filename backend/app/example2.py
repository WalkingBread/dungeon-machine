from logic.game.character import PlayerCharacter
from logic.game.game_master import GameMaster

players = [PlayerCharacter(0, "Marek", "A strong warrior standing tall", 80)]

gm = GameMaster()
gm.create_game("", players)
gm.introduce_story()

# init done

gm.start_next_scene()
gm.handle_player_action(players[0], "I am shouting like crazy to rise the attention of the nearby people!")

for scene in gm.story:
    print(scene.get_scene_content())

print("i use this as debugging breakpoint :)")