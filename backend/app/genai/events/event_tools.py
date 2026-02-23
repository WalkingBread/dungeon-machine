from langchain.tools import tool
from app.logic.character.stat import StatType
from app.logic.gameflow.game_state import GameState
from app.models.event import EventType, DiceEvent, HealthEvent
import logging

@tool
def publish_dice_event(player_name: str, related_attribute: StatType):
    """
    A tool prepared for an LLM to publish an event that will be executed after
    text generation. This one is used to request a dice roll from a player.
    Args:
        player_name - name of the player that will roll the dice
        related_attribute - an attribute from the enum that should be used for the roll
    """
    game_state = GameState.get_game_state()
    event = DiceEvent((EventType.DICE_EVENT), player_name, related_attribute)
    game_state.publish_to_event_queue(event)
    logging.info(f"Event {event} has been posted successfully")
    return f"Event {event} has been posted successfully" # for the llm to go forward

@tool
def publish_health_event(player_name: str, value_change: int):
    """
    A tool prepared for an LLM to publish an event that will be executed after
    text generation. This one is used to change the value by a specific amount.
    Args:
        player_name - name of the player that will be affected by health change
        value_change - the amount of the health change made to the player, to decrement use negatvie values.
    """
    game_state = GameState.get_game_state()
    event = HealthEvent((EventType.HEALTH_EVENT), player_name, value_change)
    game_state.publish_to_event_queue(event)
    logging.info(f"Event {event} has been posted successfully")
    return f"Event {event} has been posted successfully" # for the llm to go forward
    
