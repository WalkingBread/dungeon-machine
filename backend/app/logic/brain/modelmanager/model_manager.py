from logic.brain.modelmanager.llm_payload_formater import prepare_llm_story_payload
from logic.brain.modelmanager.prompts import get_storyteller_prompt, get_reaction_prompt
from genai.models import get_gpt_five, get_gpt_five_mini
from logic.brain.modelmanager.request_structures import StoryUpdate, PlayerActionOutcomes
from logic.brain.modelmanager.v2.chains import build_chain_registry, Node
from logic.brain.modelmanager.v2.response_models import ActionDecision, RollRequirement, RollConsequence, FinalSummary

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

        self._action_chain_registry = build_chain_registry(get_gpt_five_mini())

    def provide_scene_setting(self, model_context: dict) -> StoryUpdate:
        llm_payload = prepare_llm_story_payload(model_context)
        return self._model_dict[STORYTELLER_MODEL_DICT_NAME].invoke(llm_payload)

    def provide_action_decision(self, model_context: dict) -> ActionDecision:
        return self._action_chain_registry[Node.DECIDER].invoke(model_context)

    def provide_action_roll(self, model_context: dict) -> RollRequirement:
        return self._action_chain_registry[Node.ROLL_SETTER].invoke(model_context)

    def provide_action_roll_outcome_description(self, model_context: dict) -> RollConsequence:
        return self._action_chain_registry[Node.ROLL_OUTCOME].invoke(model_context)

    def provide_action_final_summary(self, model_context: dict) -> FinalSummary:
        return self._action_chain_registry[Node.FINALIZER].invoke(model_context)
        
