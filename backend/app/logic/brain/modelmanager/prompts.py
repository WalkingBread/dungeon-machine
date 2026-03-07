import json

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


def get_storyteller_prompt() -> ChatPromptTemplate:
    system_message = (
        "You are a Master Storyteller and Game Engine logic mapper. "
        "Your job is to advance the story and translate narrative actions into engine events.\n\n"
        "RULES:\n"
        "1. Narrative: Keep the tone dark and adventurous.\n"
        "2. AddCharacter: Use this when a new named entity enters the scene.\n"
        "3. ChangeHealth: Use negative values for damage and positive for healing.\n"
        "4. DeleteCharacter: Use this only when a character dies or permanently leaves.\n\n"
        "5. Text length: For a scene description try to generate between 100 and 200 words.\n\n"
        "6. Questions: Don't add explicit questions to the player.\n\n"
        "7. Event Type: Don't forget to add event_type literal to each of the event objects.\n\n"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "## Current Game State:\n {model_context}")
    ])
    return prompt

def get_reaction_prompt() -> ChatPromptTemplate:
    examples = [
        {
            "model_context": json.dumps({
                "pending_actions": [{
                    "player": "Valerius",
                    "player_intent": "I try to pick the lock on the heavy iron chest.",
                    "completed_steps": [],
                    "active_event": None
                }]
            }),
            "output": json.dumps({
                "character_outcomes": {
                    "Valerius": {
                        "description": "You kneel before the chest, feeling for the tumblers with your picks.",
                        "rolls": [{"event_type": "dice_roll", "character_name": "Valerius", "statistic": "AGILITY"}]
                    }
                }
            })
        },
        {
            "model_context": json.dumps({
                "pending_actions": [{
                    "player": "Valerius",
                    "player_intent": "I try to pick the lock on the heavy iron chest.",
                    "completed_steps": [],
                    "active_event": {"stat": "AGILITY", "result": "SUCCESS"}
                }]
            }),
            "output": json.dumps({
                "character_outcomes": {
                    "Valerius": {
                        "description": "With a satisfying click, the lock yields. You throw the lid back. Let's see what's inside.",
                        "rolls": [{"event_type": "dice_roll", "character_name": "Valerius", "statistic": "LUCK"}]
                    }
                }
            })
        },
        {
            "model_context": json.dumps({
                "pending_actions": [{
                    "player": "Valerius",
                    "player_intent": "I try to pick the lock on the heavy iron chest.",
                    "completed_steps": [{
                        "stat": "AGILITY",
                        "result": "SUCCESS",
                        "description": "With a satisfying click, the lock yields. You throw the lid back."
                    }],
                    "active_event": {"stat": "LUCK", "result": "EXTREME_FAILURE"}
                }]
            }),
            "output": json.dumps({
                "character_outcomes": {
                    "Valerius": {
                        "description": "The chest is empty save for a few cobwebs and a mocking note. You've wasted your time and a good pick.",
                        "rolls": []
                    }
                }
            })
        },
        {
            "model_context": json.dumps({
                "pending_actions": [{
                    "player": "Valerius",
                    "player_intent": "I try to pick the lock.",
                    "completed_steps": [],
                    "active_event": {"stat": "AGILITY", "result": "EXTREME_FAILURE"}
                }]
            }),
            "output": json.dumps({
                "character_outcomes": {
                    "Valerius": {
                        "description": "The pick snaps, and a needle trap springs from the keyhole, piercing your hand!",
                        "rolls": [{"event_type": "change_health", "character_name": "Valerius", "health_amount": -5}]
                    }
                }
            })
        }
    ]

    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "## Game Context\n {model_context}"),
        ("ai", "{output}")
    ])

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    system_message = (
        "You are the Game Master. Your job is to drive the story forward by responding to player actions. "
        "Every time you respond, you must make a choice: \n\n"
        "1. IS THE ACTION FINISHED? If the player's intent is fully resolved by the current dice results, "
        "describe the final outcome and include any 'change_health' events if they were hurt or healed.\n"
        "2. IS ANOTHER ROLL NEEDED? If the player's intent requires more effort (e.g., they hit but need to "
        "roll for damage, or they opened a chest but need to roll for luck), provide a description of current "
        "status and add a new 'dice_roll' event to the list.\n\n"
        "Always look at 'completed_steps' to see what has already happened so you don't repeat yourself."
    )

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        few_shot_prompt,
        ("human", "## Game Context\n {model_context}"),
    ])