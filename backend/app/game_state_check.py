from dotenv import load_dotenv
from app.logic.character.character import Character
from app.genai.models import get_gpt_five
from app.genai.events.event_tools import publish_dice_event, publish_health_event
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from app.logic.gameflow.game_state import GameState

load_dotenv()

if __name__ == "__main__":
    print("halo")
    character1 = Character.generate_character("Mateus")
    character2 = Character.generate_character("Michall")
    char_list = [character1, character2]

    intro_text = """Mateus and Michall stood at the mouth of the Sunken Crypt, 
    their shadows stretching long against the moss-covered stone. 
    A low, rhythmic thrumming vibrated through the floorboards, 
    signaling that the ritual had already begun. With a shared 
    nod of grim determination, they drew their steel and stepped 
    into the dark."""
    intro_text2 = """Steel clashes against bone as Mateus and Michall surge into the 
    Sunken Crypt. A jagged obsidian shard, propelled by the ritual's pulsing energy, 
    slices through the air toward Mateus's chest. Meanwhile, a hulking Crypt 
    Guardian slams its mace into the stone floor, the shockwave threatening to 
    knock Michall off his feet. The air is thick with the copper scent of blood 
    and the stinging ozone of dark magic. The battle for the Crypt is joined."""

    game_log = [intro_text, intro_text2]
    game_state = GameState(char_list, intro_text)

    llm = get_gpt_five()
    tools = [publish_health_event, publish_dice_event]
    agent = create_agent(llm, tools=tools)

    game_prompt = ChatPromptTemplate.from_messages([
        ("system",
        "You are an expert Dungeon Master and interactive storyteller. "
        "Your goal is to progress the story based on user input while maintaining a consistent world state.\n\n"
        "Rules for Interaction:\n"
        "1. Narrative Flow: Describe the environment and the consequences of the user's actions vividly.\n"
        "2. Tool Usage: You have access to tools that trigger game events (dice rolls, health changes). "
        "If a user's action requires a formal mechanic, call the appropriate tool and finish generation\n"
        "4. Agency: Do not make decisions for the player character; describe the world's reaction to their choices.\n"
        "5. Additional information: You will be provided with: user's character objects and game log, explaining current game history.\n"
        ),
        ("user", "{input}")
    ])

    char_data = "\n".join([
        f"Name: {c.name}, Health: {c.health}, Stats: {c.stats}"
        for c in char_list
    ])

    history_text = "\n".join(game_log)

    context_input = f"""
    ### PARTY STATUS ###
    {char_data}

    ### GAME HISTORY ###
    {history_text}
    """

    chain = game_prompt | agent

    response = chain.invoke({"input": context_input})

    final_message = response["messages"][-1].content
    game_log.append(final_message)
    print(final_message)
    print(response)
