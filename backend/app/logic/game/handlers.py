from logic.character import Character
from logic.game.character import GameCharacter
from logic.game.game_event import HealthEvent, AddCharacterEvent, RemoveCharacterEvent

def handle_health_change(game: 'Game', event: HealthEvent):
    target: GameCharacter = next(
        (c for c in list(game.player_characters) + game.npc_characters
         if c.name == event.character_name),
        None
    )
    if target:
        target.health += event.health_change

def handle_add_character(game: 'Game', event: AddCharacterEvent):
    if not any(c.name == event.character_name for c in game.npc_characters):
        new_npc = Character.generate_character(event.character_name)
        new_npc.max_health = event.health_points
        new_npc.health = event.health_points
        game.npc_characters.append(new_npc)

def handle_remove_character(game: 'Game', event: RemoveCharacterEvent):
    game.npc_characters = [
        c for c in game.npc_characters
        if c.name != event.character_name
    ]

EVENT_HANDLERS = {
    HealthEvent: handle_health_change,
    AddCharacterEvent: handle_add_character,
    RemoveCharacterEvent: handle_remove_character,
}
