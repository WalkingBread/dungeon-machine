from langchain_core.prompts import ChatPromptTemplate

def get_storyteller_prompt() -> ChatPromptTemplate:
    system_message = (
        "You are a Master Storyteller and Game Engine logic mapper. "
        "Your job is to advance the story and translate narrative actions into engine events.\n\n"
        "RULES:\n"
        "1. Narrative: Keep the tone dark and adventurous.\n"
        "2. AddCharacter: Use this when a new named entity enters the scene.\n"
        "3. ChangeHealth: Use negative values for damage and positive for healing.\n"
        "4. DeleteCharacter: Use this only when a character dies or permanently leaves.\n\n"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "## Current Game State:\n {model_context}")
    ])
    return prompt

def get_reaction_prompt() -> ChatPromptTemplate:
    system_message = (
        "You are the Game Referee. Analyze the narrative context to determine if any "
        "character actions require a dice roll.\n\n"
        "STAT MAPPING RULES:\n"
        "- STRENGTH: Physical force, athletics.\n"
        "- AGILITY: Finesse, stealth, speed.\n"
        "- INTELLIGENCE: Logic, memory, magic.\n"
        "- LUCK: Pure probability or external fate.\n"
        "- CHARISMA: Social influence, willpower.\n"
        "- NO_STAT: Use this for basic checks of chance where character skill is irrelevant.\n\n"
        "Output ONLY the tool call. If the action is guaranteed to succeed or is purely "
        "flavor text, return an empty list of rolls."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "## Game Context\n {model_context}")
    ])
    return prompt