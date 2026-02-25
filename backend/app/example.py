from logic.game import GameMaster
from logic.game.player import Player
from logic.character import Character
from logic.modelmanager import ModelManagerConfiguredImpl

brain = ModelManagerConfiguredImpl()

gm = GameMaster(brain)

players: list[Player] = [Character.generate_character('Adam')]

gm.create_game('Some random theme', players)
scene1 = gm.introduce_story()
# print(scene1.to_dict())
# print('----------')
state = gm.execute_player_action(players[-1], 'I try to find someone to talk to.')
# print(state.to_dict())
#print('----------')
scene2 = gm.provide_scene()
#print(scene2.to_dict())
print(gm._history[-1].to_dict())