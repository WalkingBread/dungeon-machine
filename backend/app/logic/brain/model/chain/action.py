from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.model.request import ActionState, RollRequirement, RollConsequence, FinalSummary
from logic.brain.model.chain.base import BaseLangChainWrapper

DECIDER_INSTRUCTION = (
    "Analyze the player's INTENT and the current ACTION_HISTORY to determine the next immediate engine state.\n"
    "CRITICAL RULES FOR FIELD POPULATION:\n"
    "1. 'state': Set to 'INPUT' if the action is a conversational step, dialogue, or safe exploration requiring more player text. "
    "Set to 'ROLL' if the action involves physical risk, skill usage, or an contested check. "
    "Set to 'FINISH' if the action is basic, instantly resolved, or if a roll for this intent was already completed in the history.\n"
    "2. 'narrative': Write a 1-2 sentence response showing how the world or NPCs immediately react to the player's intent.\n"
    "3. 'engine_events': Include any structural modifications to the environment or characters resulting from this interaction."
)

ROLL_OUTCOME_INSTRUCTION = (
    "The player rolled a {result} for their required stat test. Evaluate the consequences.\n"
    "CRITICAL RULES FOR FIELD POPULATION:\n"
    "1. 'narrative': Write a single, punchy sentence describing the immediate physical or social layout change caused by this roll result.\n"
    "2. 'state': Determine the next phase of the transaction: "
    "Set to 'INPUT' if the roll's result forces a conversational opening (e.g., an NPC demands an immediate answer). "
    "Set to 'ROLL' if the outcome triggers a cascading physical emergency requiring an immediate follow-up save. "
    "Set to 'FINISH' if the action path is fully resolved and the turn is complete.\n"
    "3. 'engine_events': Populate with mechanical changes matching the narrative (e.g., ChangeHealth if they failed a hazard check)."
)

ROLL_SETTER_INSTRUCTION = (
    "Identify the single most logical statistic required for this active attempt. "
    "Write a narrative 'intro' sentence that builds suspense around the attempt."
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
        super().__init__(llm, DECIDER_INSTRUCTION, ActionState)

class RollOutcomeActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, ROLL_OUTCOME_INSTRUCTION, ActionState)

class RollSetterActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, ROLL_SETTER_INSTRUCTION, RollRequirement)

class FinalizerActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, FINALIZER_INSTRUCTION, FinalSummary)