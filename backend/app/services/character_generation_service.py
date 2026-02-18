from langchain_core.prompts import ChatPromptTemplate
from ..genai.models import get_gpt_five
from app.models.character import Character


def generate_character(description: str):
    character_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a D&D character generator.\n"
         "Generate a character object based on the description provided by the user.\n"
         "Make sure that the average strength + agility + intelligence + luck + charisma stays about 5 points.\n"
         ),
        ("user", "{input}")
    ])
    llm = get_gpt_five().with_structured_output(Character)
    character_generation_chain = character_prompt | llm
    return character_generation_chain.invoke({"input": description})