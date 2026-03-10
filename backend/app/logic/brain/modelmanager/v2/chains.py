from enum import Enum, auto

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.modelmanager.v2.response_models import RollConsequence, FinalSummary, RollRequirement, ActionDecision

class Node(Enum):
    DECIDER = auto()
    ROLL_SETTER = auto()
    ROLL_OUTCOME = auto()
    FINALIZER = auto()

PROMPT_REGISTRY = {
    Node.DECIDER: {
        "instruction": (
            "Analyze the INTENT and ACTION_HISTORY. "
            "Return 'FINISH' if the situation has escalated to a point where the original intent "
            "is either resolved, impossible, or has been replaced by a more urgent threat (like a fight or injury). "
            "A 'CRITICAL' or 'EXTREME' failure should almost always result in 'FINISH' because the "
            "consequences should fundamentally change the scene."
            "SAFETY RULE: This is a slapstick comedy fantasy. "
            "NEVER use words related to gore, soul-draining, or realistic injury."
        ),
        "schema": ActionDecision
    },
    Node.ROLL_SETTER: {
        "instruction": "Identify the required statistic for the next step and write a narrative 'intro' sentence that "
                       "builds suspense.",
        "schema": RollRequirement
    },
    Node.ROLL_OUTCOME: {
        "instruction": "The player rolled a {result}. Describe the immediate physical consequence in one punchy "
                       "sentence.",
        "schema": RollConsequence
    },
    Node.FINALIZER: {
        "instruction": "Synthesize the intent and all turn history into a cohesive 2-3 sentence final narrative "
                       "paragraph.",
        "schema": FinalSummary
    }
}

def build_chain_registry(llm: BaseChatModel) -> dict[Node, Runnable]:
    registry = {}

    for node, data in PROMPT_REGISTRY.items():
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "You are a fantasy TTRPG Engine. "
                                          "Return the valid result based upon response schema and TASK section"
                                        "Maintain a PG-13 adventure tone. Focus on high-stakes drama and "
                                        "fantasy action rather than graphic or realistic violence. "
                                        "Do not describe gore or excessive cruelty."
                                          "SAFETY RULE: This is a slapstick comedy fantasy. "
                                          "NEVER use words related to gore, soul-draining, or realistic injury."
             },
            ("user", "## SCENE_CONTEXT:\n{scene}"),
            ("user", "## GAME_STATE:\n{game_state}"),
            ("user", "## PLAYER_INTENT:\n{intent}"),
            ("user", "## ACTION_HISTORY:\n{action_history}"),
            ("user", f"## TASK:\n{data['instruction']}")
        ])

        chain = prompt | llm.with_structured_output(data["schema"])

        registry[node] = chain

    return registry