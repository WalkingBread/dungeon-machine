import logging
import pytest
import json
from logic.character import Character
from logic.character.stat import StatType
from logic.dice import TestRollOutcome
from logic.game.character import GameCharacter, PlayerCharacter
from logic.game.game import GameState
from logic.game.player_action import PlayerAction, ActionVerificationException
from logic.game.scene import Scene, GameIntroductionSequence
from logic.brain.context.parser import (
    SceneSettingParser, 
    PlayerActionParser, 
    RollOutcomeParser
)


@pytest.fixture
def setup_game_data():
    character: PlayerCharacter = Character.generate_character(name="Valerius")
    state = GameState(theme="Fantasy", player_characters=[character], npc_characters=[])
    
    scene = Scene()
    scene.add(GameIntroductionSequence("You stand before the Iron Gate of Galdur."))
    
    return [scene], state


def test_character_to_json_serialization():
    parser = SceneSettingParser()
    character: GameCharacter = Character.generate_character("Test Character")
    
    parsed = parser._parse_character_to_json(character)
    
    data = json.loads(parsed)
    assert data["name"] == "Test Character"
    assert "health" in data
    assert "statistics" in data
    logging.info(f"Parsed character: {parsed}")


def test_scene_setting_parser(setup_game_data):
    story, game_state = setup_game_data
    parser = SceneSettingParser()
    
    context = parser.parse(story=story, game_state=game_state)
    
    assert "scene" in context
    assert "game_state" in context
    assert "Valerius" in context["game_state"]
    assert "Iron Gate" in context["scene"]


def test_player_action_history_step_by_step():
    parser = PlayerActionParser()
    action = PlayerAction(player_name="Kaelen")
    
    action.add_player_action("I try to sneak.")
    
    action.add_new_dice_roll(StatType.LUCK, "Checking floor.")
    action.add_result_to_dice_roll(TestRollOutcome.SUCCESS)
    
    history = parser._parse_action_history(action)
    assert "ROLL 1 (LUCK)" in history
    assert "Result: SUCCESS" in history
    logging.info(f"History Log:\n{history}")

def test_player_action_parser_full_context(setup_game_data):
    story, game_state = setup_game_data
    parser = PlayerActionParser()
    
    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I pick the lock.")
    
    context = parser.parse(story=story, action=action, game_state=game_state)
    
    assert "intent" in context
    assert "action_history" in context
    assert "Valerius wants to: I pick the lock" in context["intent"]

def test_roll_outcome_parser_includes_result(setup_game_data):
    story, game_state = setup_game_data
    parser = RollOutcomeParser()
    
    action = PlayerAction(player_name="Valerius")
    action.add_player_action("I attack.")
    action.add_new_dice_roll(StatType.STRENGTH, "Hammer swing.")
    action.add_result_to_dice_roll(TestRollOutcome.EXTREME_SUCCESS)
    
    context = parser.parse(story=story, action=action, game_state=game_state)
    
    assert "intent" in context
    assert context["result"] == "EXTREME_SUCCESS"
    logging.info(f"Outcome Context: {context['result']}")


def test_action_validation_failure(setup_game_data):
    story, game_state = setup_game_data
    parser = PlayerActionParser()

    action = PlayerAction(player_name="Valerius")
    action.player_action = "no"

    with pytest.raises(ActionVerificationException):
        parser.parse(story=story, action=action, game_state=game_state)