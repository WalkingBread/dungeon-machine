from logic.character import Character
from logic.game.event import HealthEvent, AddCharacterEvent, RemoveCharacterEvent, GameEvent

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logic.game.game import Game

class EventHandlerManager:
    def __init__(self, game: Game):
        self.game = game
        self._event_handlers = {
            HealthEvent: HealthEventHandler(),
            AddCharacterEvent: AddCharacterEventHandler(),
            RemoveCharacterEvent: RemoveCharacterEventHandler()
        }

    def handle_event(self, event: GameEvent):
        event_handler = self._event_handlers.get(type(event))
        if event_handler:
            event_handler.handle_event(self.game, event)


class GameEventHandler(ABC):
    
    @abstractmethod
    def handle_event(self, game: Game, event: GameEvent):
        pass


class HealthEventHandler(GameEventHandler):
    
    def handle_event(self, game: Game, event: HealthEvent):
        character = game.get_character(event.character_name)
        if character:
            character.change_health(event.health_change)


class AddCharacterEventHandler(GameEventHandler):

    def handle_event(self, game: Game, event: AddCharacterEvent):
        if not game.get_npc(event.character_name):
            new_npc = Character.generate_character(event.character_name)
            new_npc.max_health = event.health_points
            new_npc.health = event.health_points
            game.npcs.append(new_npc)


class RemoveCharacterEventHandler(GameEventHandler):

    def handle_event(self, game: Game, event: AddCharacterEvent):
        character = game.get_npc(event.character_name)
        if character:
            game.npcs.remove(character)