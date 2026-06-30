from genai.provider import ModelProvider, Model
from logic.brain.model.chain.story import StoryUpdateChain, StoryIntroChain
from logic.brain.model.request import (
    StoryUpdate, 
    ActionState,
    RollRequest, 
    FinalSummary
)
from logic.brain.model.chain.action import (
    DeciderActionChain,
    RollOutcomeActionChain,
    RollSetterActionChain,
    FinalizerActionChain
)

from logic.brain.model.chain.type import ChainType

"""
This class and the module overall is used for configuration of the direct requests
going to the llm the chains are build at modelmanagaer/chains and the returned objects
can be configured at request.structures.py.
The configuration of the used models is done via this constructor.
"""
class ModelManager:
    def __init__(self):
        model_provider = ModelProvider()

        storyteller_model = model_provider.get_model(Model.GPT_5_MINI)
        action_model = model_provider.get_model(Model.GPT_5_MINI)

        self._chains = {
            ChainType.DECIDER: DeciderActionChain(action_model),
            ChainType.ROLL_SETTER: RollSetterActionChain(action_model),
            ChainType.ROLL_OUTCOME: RollOutcomeActionChain(action_model),
            ChainType.FINALIZER: FinalizerActionChain(action_model),
            ChainType.STORY_UPDATE: StoryUpdateChain(storyteller_model),
            ChainType.STORY_INTRO: StoryIntroChain(storyteller_model)
        }

    def provide_story_intro(self, model_context: dict) -> StoryUpdate:
        return self._chains[ChainType.STORY_INTRO].invoke(model_context)

    def provide_scene_setting(self, model_context: dict) -> StoryUpdate:
        return self._chains[ChainType.STORY_UPDATE].invoke(model_context)

    def provide_action_decision(self, model_context: dict) -> ActionState:
        return self._chains[ChainType.DECIDER].invoke(model_context)

    def provide_action_roll(self, model_context: dict) -> RollRequest:
        return self._chains[ChainType.ROLL_SETTER].invoke(model_context)

    def provide_action_roll_outcome_description(self, model_context: dict) -> ActionState:
        return self._chains[ChainType.ROLL_OUTCOME].invoke(model_context)

    def provide_action_final_summary(self, model_context: dict) -> FinalSummary:
        return self._chains[ChainType.FINALIZER].invoke(model_context)