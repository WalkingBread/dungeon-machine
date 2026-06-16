from logic.brain.model.chains.storyteller_chain import StorytellerChain
from genai.provider import ModelProvider, Model
from logic.brain.model.request_structures import (
    StoryUpdate, 
    ActionDecision,
    RollRequirement, 
    RollConsequence, 
    FinalSummary
)
from logic.brain.model.chains.action_chains import ActionChainRegistry, Node

STORYTELLER_MODEL_DICT_NAME = "storyteller_model"

class ModelManager:
    def __init__(self):
        """
        This class and the module overall is used for configuration of the direct requests
        going to the llm the chains are build at modelmanagaer/chains and the returned objects
        can be configured at request.structures.py.
        The configuration of the used models is done via this constructor.
        """

        model_provider = ModelProvider()

        self.storyteller_chain = StorytellerChain(model_provider.get_model(Model.GPT_5_MINI))
        self._action_chain_registry = ActionChainRegistry(model_provider.get_model(Model.GPT_5_MINI))

    def provide_scene_setting(self, model_context: dict) -> StoryUpdate:
        return self.storyteller_chain.invoke(model_context)

    def provide_action_decision(self, model_context: dict) -> ActionDecision:
        return self._action_chain_registry[Node.DECIDER].invoke(model_context)

    def provide_action_roll(self, model_context: dict) -> RollRequirement:
        return self._action_chain_registry[Node.ROLL_SETTER].invoke(model_context)

    def provide_action_roll_outcome_description(self, model_context: dict) -> RollConsequence:
        return self._action_chain_registry[Node.ROLL_OUTCOME].invoke(model_context)

    def provide_action_final_summary(self, model_context: dict) -> FinalSummary:
        return self._action_chain_registry[Node.FINALIZER].invoke(model_context)