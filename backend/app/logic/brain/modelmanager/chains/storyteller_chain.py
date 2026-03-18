from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.modelmanager.request_structures import StoryUpdate


def build_storyteller_chain(llm: BaseChatModel) -> Runnable:
    """
    This function is used to build the storyteller chain, you can configure the
    system prompt in the body, to configure the returned object you need to
    adjust request_structures.py.
    """
    system_message = (
        "You are a Master Storyteller for a tabletop roleplaying game. "
        "Maintain a PG-13 adventure tone. Focus on high-stakes drama and "
        "fantasy action rather than graphic or realistic violence. "
        "NEVER use words related to gore, soul-draining, or realistic injury."
        "RULES:\n"
        "1. CLARITY: Use simple, direct language. Avoid complex metaphors.\n"
        "2. LENGTH: Keep scene descriptions under 60 words. Be brief.\n"
        "3. SENSES: Describe one thing the player sees, hears, and smells.\n"
        "4. ENGINE LOGIC: Translate actions into events (AddCharacter, DeleteCharacter).\n"
        "5. NO QUESTIONS: Do not ask the player what they do; the engine handles that.\n"
        "6. EVENT TYPES: Include the 'event_type' literal in every event object.\n"
        "7. LANGUAGE: Use simple english to describe the scenes don't add too much old vocabulary.\n"
        "TONE: Gritty, medieval, and high-stakes."
    )

    prompt = ChatPromptTemplate.from_messages([
        {"role": "system", "content": system_message
         },
        ("user", "## PREVIOUS_SCENE_CONTEXT:\n{scene}"),
        ("user", "## GAME_STATE:\n{game_state}"),
    ])

    storyteller_chain = (
            prompt | llm.with_structured_output(
        StoryUpdate,
        method="function_calling")
    )

    return storyteller_chain
