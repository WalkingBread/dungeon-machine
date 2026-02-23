import pytest
import logging
from app.logic.modelmanager.configured.model_manager_configured_impl import ModelManagerConfiguredImpl
from app.logic.modelmanager.configured.models import StoryUpdate

logger = logging.getLogger(__name__)

class TestModelManagerConfiguredImpl:

    @pytest.fixture
    def manager(self):
        return ModelManagerConfiguredImpl()

    @pytest.fixture
    def full_context(self):
        """
        Synthesizing the complex context:
        - Player info
        - Game character info (NPCs)
        - Previous story segment
        - Dice rolls requested & results
        """
        return {
            "player_characters": [
                {"name": "Grog", "class": "Barbarian", "health": 150 ,
                 "stats": {"STRENGTH": 29, "AGILITY": 12, "INTELLIGENCE": 3, "LUCK": 3, "CHARISMA": 18}}
            ],
            "non_player_characters": [
                {"name": "The Weeping Willow", "health": 200, "alignment": "Hostile"}
            ],
            "previous_scene_description": "The forest grew silent as the ancient tree began to stir.",
            "user_prompt": "I swing my axe with everything I've got to cleave the corrupted roots!",
            "last_dice_rolls": [
            {
                "character": "Grog",
                "stat": "STRENGTH",
                "natural_roll": 15,
                "modifier": 4,
                "total": 19,
                "intent": "Cleave the corrupted roots"
            }
        ],
        }

    @pytest.fixture
    def user_action_context(self):
        """
        Synthesizing the part complex context:
        - Player info
        - Game character info (NPCs)
        - User requested actions
        """
        return {
            "player_characters": [
                {"name": "Grog", "class": "Barbarian", "health": 150,
                 "stats": {"STRENGTH": 29, "AGILITY": 12, "INTELLIGENCE": 3, "LUCK": 3, "CHARISMA": 18}}
            ],
            "non_player_characters": [
                {"name": "The Weeping Willow", "health": 200, "alignment": "Hostile"}
            ],
            "user_prompt": "I swing my axe with everything I've got to cleave the corrupted roots!",
        }

    def test_provide_scene_description_integration(self, manager, full_context):
        """
        Tests the storyteller chain.
        Logs the generated story and events for inspection.
        """
        try:
            # Act
            response = manager.provide_scene_description(full_context)

            # Log results (visible with pytest -s)
            print(f"\n--- STORYTELLER OUTPUT ---")
            print(f"STORY: {response.new_story_segment}")
            print(f"ENGINE EVENTS: {response.engine_events}")

            # Assertions: Verify type and schema adherence
            assert isinstance(response, StoryUpdate), "Should return a StoryUpdate instance"
            assert isinstance(response.new_story_segment, str)
            assert isinstance(response.engine_events, list)

        except Exception as e:
            pytest.fail(f"Storyteller chain crashed or failed validation: {e}")

    def test_provide_character_events_integration(self, manager, user_action_context):
        """
        Tests the reaction chain.
        Logs the generated events for inspection.
        """
        try:
            response = manager.provide_character_events(user_action_context)

            print(f"\n--- REACTION OUTPUT ---")
            print(f"ROLLS REQUESTED: {response.rolls}")

            from app.logic.modelmanager.configured.models import RollDecision, StatType

            assert isinstance(response, RollDecision), "Should return a RollDecision instance"
            assert isinstance(response.rolls, list), "Rolls should be a list"

            if len(response.rolls) > 0:
                first_roll = response.rolls[0]
                assert hasattr(first_roll, 'character_name'), "Roll must specify a character"
                assert isinstance(first_roll.statistic, StatType), "Statistic must be a valid StatType Enum"
                print(f"Validated Roll: {first_roll.character_name} via {first_roll.statistic}")

        except Exception as e:
            pytest.fail(f"Reaction chain (Dice Master) crashed or failed validation: {e}")