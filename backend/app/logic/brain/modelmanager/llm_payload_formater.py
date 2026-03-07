import yaml

def prepare_llm_story_payload(model_context: dict) -> str:
    """
    Takes a game state dict, cleans it, and returns a
    Markdown-formatted string with YAML blocks.
    """

    def clean(data):
        if isinstance(data, dict):
            cleaned_dict = {k: clean(v) for k, v in data.items()}
            return {k: v for k, v in cleaned_dict.items()
                    if v is not None and v != "" and v != {} and v != []}
        elif isinstance(data, (list, tuple, set)):
            cleaned_list = [clean(i) for i in data]
            return [i for i in cleaned_list if i is not None and i != ""]
        return data

    cleaned_data = clean(model_context)
    output_parts = []

    for category, content in cleaned_data.items():
        # Capitalize header for better LLM attention (e.g., 'STORY')
        header = f"### {category.upper()}"

        yaml_block = yaml.dump(
            content,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True
        )

        section = f"{header}\n```yaml\n{yaml_block}```"
        output_parts.append(section)

    return "\n\n".join(output_parts)
