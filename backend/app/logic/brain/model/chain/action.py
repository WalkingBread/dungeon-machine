from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.model.request_structures import ActionDecision, RollRequirement, RollConsequence, FinalSummary
from logic.brain.model.chain.base import BaseLangChainWrapper

DECIDER_INSTRUCTION = (
    "Analyze the INTENT and ACTION_HISTORY. "
    "Determine if the player's action is a basic interaction (like speaking, looking around, or introducing themselves) "
    "or an active attempt at something risky requiring a skill roll (like lying, sneaking, hacking, or fighting).\n"
    "Return 'CONTINUE' for casual dialogue or simple actions that do not require a roll.\n"
    "Only return 'FINISH' if the scene has physically concluded, transitioned to an entirely new location, "
    "or entered structural combat initiative tracking."
)

ROLL_SETTER_INSTRUCTION = (
    "Identify the single most logical statistic required for this active attempt. "
    "Do NOT require rolls for simple speech or greeting NPCs. If a roll IS necessary, "
    "write a narrative 'intro' sentence that builds suspense around the attempt."
)

ROLL_OUTCOME_INSTRUCTION = (
    "The player rolled a {result}. Describe the immediate physical or social consequence in one punchy sentence. "
    "If the roll was a FAILURE, introduce a narrative complication or an escalating threat (e.g., an NPC draws a weapon) "
    "instead of instantly breaking the plot or destroying key quest items."
)

FINALIZER_INSTRUCTION = (
    "Synthesize the intent and all turn history into a cohesive 2-3 sentence final narrative paragraph. "
    "Ensure the paragraph ends with an active conversational prompt, a shift in NPC posture, or a clear environmental "
    "cue that naturally invites the player's next move."
)

class ActionChain(BaseLangChainWrapper):

    def __init__(self, llm, instruction: str, response_schema):
        super().__init__(llm)
        self.instruction = instruction
        self.response_schema = response_schema

    def _compile_chain(self) -> Runnable:
        system_message = (
            "You are a Master TTRPG Engine. Process actions like a flexible Game Master in Dungeons & Dragons. "
            "Maintain a PG-13 adventure tone focusing on high-stakes space-fantasy drama. "
            "Never penalize players mechanically for standard, non-hostile roleplay. "
            "Return the valid JSON result based exactly upon the provided response schema and TASK section."
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