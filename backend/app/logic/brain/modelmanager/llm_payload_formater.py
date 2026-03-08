import json


def prepare_llm_story_payload(model_context: dict) -> str:
    """
    Takes a game state dict and returns a clean JSON string.
    We stop being aggressive so we don't delete the data we need.
    """

    def clean(data):
        # 1. Handle Dictionaries
        if isinstance(data, dict):
            # We only want to filter out literal None or empty strings.
            # We KEEP empty lists [] and empty dicts {} so the LLM sees the structure.
            return {
                k: clean(v) for k, v in data.items()
                if v is not None and v != ""
            }

        # 2. Handle Lists/Iterables
        elif isinstance(data, (list, tuple, set)):
            return [clean(i) for i in data if i is not None and i != ""]

        # 3. Handle Base Types
        return data

    cleaned_data = clean(model_context)

    # Fallback to empty dict if something went horribly wrong
    if not isinstance(cleaned_data, dict):
        cleaned_data = {}

    # Crucial: Return a dictionary wrapped in the key your prompt expects
    # Your prompt uses: ("human", "## Game Context\n {model_context}")
    # So we MUST return a dict where the key matches the prompt variable.
    return json.dumps(cleaned_data, ensure_ascii=False, indent=2)