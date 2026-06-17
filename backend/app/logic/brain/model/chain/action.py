from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.model.request_structures import ActionDecision, RollRequirement, RollConsequence, FinalSummary
from logic.brain.model.chain.base import BaseLangChainWrapper

DECIDER_INSTRUCTION = (
    "Analyze the INTENT and ACTION_HISTORY. "
    "Return 'FINISH' if the current interaction scenario has reached a natural conclusion, "
    "is resolved, impossible, or has transitioned into a brand-new phase (such as moving "
    "locations or entering an encounter tracking state). "
    "A low-tier mechanical outcome or severe setback should almost always result in 'FINISH' "
    "because the narrative redirection should fundamentally transition the scene layout."
)

ROLL_SETTER_INSTRUCTION = "Identify the required statistic for the next step and write a narrative 'intro' sentence that builds suspense."

ROLL_OUTCOME_INSTRUCTION = "The player rolled a {result}. Describe the immediate physical consequence in one punchy sentence."

FINALIZER_INSTRUCTION = "Synthesize the intent and all turn history into a cohesive 2-3 sentence final narrative paragraph."

class ActionChain(BaseLangChainWrapper):

    def __init__(self, llm, instruction: str, response_schema):
        super().__init__(llm)
        self.instruction = instruction
        self.response_schema = response_schema

    def _compile_chain(self) -> Runnable:
        system_message = (
            "You are a fantasy TTRPG Engine. "
            "Return the valid result based upon response schema and TASK section"
            "Maintain a PG-13 adventure tone. Focus on high-stakes drama"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": system_message},
            ("user", "## SCENE_CONTEXT:\n{scene}"),
            ("user", "## GAME_STATE:\n{game_state}"),
            ("user", "## PLAYER_INTENT:\n{intent}"),
            ("user", "## ACTION_HISTORY:\n{action_history}"),
            ("user", f"## TASK:\n{self.instruction}")
        ])
        
        return prompt | self.llm.with_structured_output(self.response_schema)
    
class DeciderActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, DECIDER_INSTRUCTION, ActionDecision)

class RollSetterActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, ROLL_SETTER_INSTRUCTION, RollRequirement)

class RollOutcomeActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, ROLL_OUTCOME_INSTRUCTION, RollConsequence)

class FinalizerActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, FINALIZER_INSTRUCTION, FinalSummary)