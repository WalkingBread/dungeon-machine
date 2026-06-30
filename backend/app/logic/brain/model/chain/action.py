from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.model.request import ActionState, RollRequest, FinalSummary
from logic.brain.model.chain.base import BaseLangChainWrapper

DECIDER_INSTRUCTION = (
    "Analyze the current SCENE_CONTEXT and player's CURRENT_ACTION to determine the next immediate engine state.\n"
    "CRITICAL RULES FOR FIELD POPULATION:\n"
    "1. 'state': Set to 'INPUT' if the interaction is an ongoing conversation, dialogue exchange, or safe observation. "
    "Set to 'ROLL' if the action directly initiates a risky physical or social challenge. "
    "Set to 'FINISH' if the player's action is minor, fully completed, or directly following a completed dice check.\n"
    "2. 'narrative': Write a 2-3 sentence response focusing purely on what happens in the physical space. "
    "If the player asked a question, have the NPC answer it through dialogue or body language. "
    "CRITICAL: Never list out explicit 'choices' or dictate what actions the player can or should perform next.\n"
    "3. 'engine_events': Track any baseline mechanical status shifts."
)

ROLL_OUTCOME_INSTRUCTION = (
    "The player rolled dice for the test. Evaluate the consequences taking into account the test result in CURRENT_ACTION and SCENE_CONTEXT as a base for further narrative. \n"
    "CRITICAL RULES FOR FIELD POPULATION:\n"
    "1. 'narrative': Write a narrative describing the immediate consequences in the story's environment caused by this roll result.\n"
    "2. 'state': Determine the next phase of player's action: "
    "Set to 'INPUT' if the roll's result forces player's text input (e.g., an NPC demands an immediate answer). "
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
            "Maintain a PG-13 adventure tone focusing on high-stakes drama. "
            "Never penalize players mechanically for standard, non-hostile roleplay. "
            "Return the valid JSON result based exactly upon the provided response schema and TASK section."
        )
        
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": system_message},
            ("user", "## SCENE_CONTEXT:\n{scene}"),
            ("user", "## GAME_STATE:\n{game_state}"),
            ("user", "## CURRENT_ACTION:\n{current_action}"),
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
        super().__init__(llm, ROLL_SETTER_INSTRUCTION, RollRequest)

class FinalizerActionChain(ActionChain):
    def __init__(self, llm):
        super().__init__(llm, FINALIZER_INSTRUCTION, FinalSummary)