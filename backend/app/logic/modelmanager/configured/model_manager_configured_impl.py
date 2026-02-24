from app.logic.modelmanager.model_manager import ModelManager
from app.logic.modelmanager.llm_payload_formater import prepare_llm_story_payload
from app.logic.modelmanager.configured.prompts import get_storyteller_prompt, get_reaction_prompt
from app.genai.models import get_gpt_five, get_gpt_five_mini
from app.logic.modelmanager.configured.models import StoryUpdate, RollDecision

STORYTELLER_MODEL_DICT_NAME = "storyteller_model"
REACTION_MODEL_DICT_NAME = "reaction_model"


class ModelManagerConfiguredImpl(ModelManager):
    def __init__(self):
        """
        All model manager configuration is done via this constructor.
        Schemas used for the events and response formats at app.logic.modelmanager.configured.models
        Prompts used for requests to each chain at app.logic.modelmanager.configured.prompts
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

    def provide_scene_description(self, model_context: dict):
        llm_payload = prepare_llm_story_payload(model_context)
        return self._model_dict[STORYTELLER_MODEL_DICT_NAME].invoke(llm_payload)

    def provide_character_events(self, model_context: dict):
        llm_payload = prepare_llm_story_payload(model_context)
        return self._model_dict[REACTION_MODEL_DICT_NAME].invoke(llm_payload)
