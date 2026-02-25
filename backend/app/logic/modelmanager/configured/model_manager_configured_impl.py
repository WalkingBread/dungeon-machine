from logic.modelmanager.model_manager import ModelManager
from logic.modelmanager.llm_payload_formater import prepare_llm_story_payload
from logic.modelmanager.configured.prompts import get_storyteller_prompt, get_reaction_prompt
from genai.models import get_gpt_five, get_gpt_five_mini
from logic.modelmanager.configured.models import StoryUpdate, RollDecision
from logic.game.scene import SceneSchema
from logic.game.action import PlayerAction, PlayerActionEvents
from logic.modelmanager.context import GameContext
from logic.game.event import GameEvent

STORYTELLER_MODEL_DICT_NAME = "storyteller_model"
REACTION_MODEL_DICT_NAME = "reaction_model"


class ModelManagerConfiguredImpl(ModelManager):
    def __init__(self):
        """
        All model manager configuration is done via this constructor.
        Schemas used for the events and response formats at logic.modelmanager.configured.models
        Prompts used for requests to each chain at logic.modelmanager.configured.prompts
        """
        self._model_dict = {}

        storyteller_chain = (
            get_storyteller_prompt() | get_gpt_five().with_structured_output(
                StoryUpdate,
                method="function_calling"
            )
        )
        self._model_dict[STORYTELLER_MODEL_DICT_NAME] = storyteller_chain

        reaction_chain = (
            get_reaction_prompt() | get_gpt_five_mini().with_structured_output(
                RollDecision,
                method="function_calling"
            )
        )
        self._model_dict[REACTION_MODEL_DICT_NAME] = reaction_chain

    def provide_scene_description(self, game_context: GameContext) -> SceneSchema:
        llm_payload = prepare_llm_story_payload(game_context.to_dict())
        story_update: StoryUpdate = self._model_dict[STORYTELLER_MODEL_DICT_NAME].invoke(llm_payload)
        return SceneSchema(
            story_update.new_story_segment,
            [GameEvent(e) for e in story_update.engine_events]
        )

    def provide_character_events(self, player_action: PlayerAction) -> PlayerActionEvents:
        llm_payload = prepare_llm_story_payload(player_action.to_dict())
        roll_decision: RollDecision = self._model_dict[REACTION_MODEL_DICT_NAME].invoke(llm_payload)
        return PlayerActionEvents(
            player_action, 
            [GameEvent(e) for e in roll_decision.rolls]
        ) 
        
