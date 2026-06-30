from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from logic.brain.model.request import StoryUpdate, StoryIntroduction
from logic.brain.model.chain.base import BaseLangChainWrapper

class StoryIntroChain(BaseLangChainWrapper):

    def _compile_chain(self) -> Runnable:
        system_message = (
            "You are a Master Storyteller for a tabletop roleplaying game. "
            "Generate an engaging, punchy, and atmospheric introduction to kick off a new adventure "
            "based upon the provided STORY SETTING.\n\n"
            "RULES:\n"
            "1. CLARITY: Use simple, evocative English. Avoid overly archaic vocabulary.\n"
            "2. LENGTH: Write a cohesive introductory narrative between 100 and 150 words. Do not be brief.\n"
            "3. SENSES: Weave in clear descriptions of what the players see, hear, and smell in this opening environment.\n"
            "4. HOOK: End the description by introducing a central conflict, mystery, or key NPC that demands immediate attention.\n"
            "5. NO QUESTIONS & NO ENGINE LOGIC: Write purely narrative prose. Do not include structural event objects or ask players what they do.\n\n"
            "TONE: Gritty, high-stakes."
        )

        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": system_message},
            ("user", "## STORY SETTING:\n{story_theme}")
        ])

        return prompt | self.llm.with_structured_output(StoryIntroduction)
    

class StoryUpdateChain(BaseLangChainWrapper):
    
    def _compile_chain(self) -> Runnable:
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
            "TONE: Gritty, high-stakes."
        )

        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": system_message},
            ("user", "## PREVIOUS_SCENE_CONTEXT:\n{scene}"),
            ("user", "## GAME_STATE:\n{game_state}"),
        ])

        return prompt | self.llm.with_structured_output(
            StoryUpdate, 
            method="function_calling"
        )