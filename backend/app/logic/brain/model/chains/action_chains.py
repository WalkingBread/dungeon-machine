from enum import Enum, auto

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.model.request_structures import ActionDecision, RollRequirement, RollConsequence, FinalSummary
from logic.brain.model.chains.base import BaseLangChainWrapper

class Node(Enum):
    DECIDER = auto()
    ROLL_SETTER = auto()
    ROLL_OUTCOME = auto()
    FINALIZER = auto()

_PROMPT_REGISTRY = {
    Node.DECIDER: {
        "instruction": (
            "Analyze the INTENT and ACTION_HISTORY. "
            "Return 'FINISH' if the current interaction scenario has reached a natural conclusion, "
            "is resolved, impossible, or has transitioned into a brand-new phase (such as moving "
            "locations or entering an encounter tracking state). "
            "A low-tier mechanical outcome or severe setback should almost always result in 'FINISH' "
            "because the narrative redirection should fundamentally transition the scene layout."
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

class ActionNodeChain(BaseLangChainWrapper):

    def __init__(self, llm, node_type: Node):
        self.node_type = node_type
        super().__init__(llm)

    def _compile_chain(self) -> Runnable:
        system_message = (
            "You are a fantasy TTRPG Engine. "
            "Return the valid result based upon response schema and TASK section"
            "Maintain a PG-13 adventure tone. Focus on high-stakes drama"
        )

        data = _PROMPT_REGISTRY[self.node_type]
        
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": system_message},
            ("user", "## SCENE_CONTEXT:\n{scene}"),
            ("user", "## GAME_STATE:\n{game_state}"),
            ("user", "## PLAYER_INTENT:\n{intent}"),
            ("user", "## ACTION_HISTORY:\n{action_history}"),
            ("user", f"## TASK:\n{data['instruction']}")
        ])
        
        return prompt | self.llm.with_structured_output(data["schema"])

class ActionChainRegistry:
    def __init__(self, llm):
        self._registry = {
            node: ActionNodeChain(llm, node) for node in Node
        }

    def __getitem__(self, item: Node) -> ActionNodeChain:
        return self._registry[item]