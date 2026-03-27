from enum import Enum, auto

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.model.request_structures import ActionDecision, RollRequirement, RollConsequence, FinalSummary


class Node(Enum):
    DECIDER = auto()
    ROLL_SETTER = auto()
    ROLL_OUTCOME = auto()
    FINALIZER = auto()

_PROMPT_REGISTRY = {
    Node.DECIDER: {
        "instruction": (
            "Analyze the INTENT and ACTION_HISTORY. "
            "Return 'FINISH' if the situation has escalated to a point where the original intent "
            "is either resolved, impossible, or has been replaced by a more urgent threat (like a fight or injury). "
            "A 'CRITICAL' or 'EXTREME' failure should almost always result in 'FINISH' because the "
            "consequences should fundamentally change the scene."
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

def build_action_chain_registry(llm: BaseChatModel) -> dict[Node, Runnable]:
    """
    This function is used to build a chain registry for the player action, it consists of the following chains:
    DECIDER: decides if an action can be finished based on the player input and current outcomes.
    ROLL_SETTER: if DECIDER decides to continue we use ROLL_SETTER to get attempt description and what roll is needed
    ROLL_OUTCOME: this node is used to get the description of the outcome of the roll
    FINALIZER: if DECIDER decides to finish the action we use this one to get a full final description of entire action
    Args:
        llm: a model used for each node
    """
    registry = {}

    system_message: str = (
        "You are a fantasy TTRPG Engine. "
        "Return the valid result based upon response schema and TASK section"
        "Maintain a PG-13 adventure tone. Focus on high-stakes drama"
    )

    for node, data in _PROMPT_REGISTRY.items():
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": system_message
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