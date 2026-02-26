from logic.brain.modelmanager.llm_payload_formater import prepare_llm_story_payload
from logic.brain.modelmanager.prompts import get_storyteller_prompt, get_reaction_prompt
from genai.models import get_gpt_five, get_gpt_five_mini
from logic.brain.modelmanager.request_structures import StoryUpdate, ActionReaction

STORYTELLER_MODEL_DICT_NAME = "storyteller_model"
REACTION_MODEL_DICT_NAME = "reaction_model"


class ModelManager:
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
                ActionReaction,
                method="function_calling"
            )
        )
        self._model_dict[REACTION_MODEL_DICT_NAME] = reaction_chain

    def provide_scene_setting(self, model_context: dict) -> StoryUpdate:
        llm_payload = prepare_llm_story_payload(model_context)
        return self._model_dict[STORYTELLER_MODEL_DICT_NAME].invoke(llm_payload)

    def provide_action_reaction(self, model_context: dict) -> ActionReaction:
        llm_payload = prepare_llm_story_payload(model_context)
        return self._model_dict[REACTION_MODEL_DICT_NAME].invoke(llm_payload)
        
