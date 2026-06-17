import json

def clean_json_response(content: str) -> dict:
    """
    Cleans raw markdown and whitespace from an LLM response and parses it to JSON.
    """
    cleaned_text = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    return json.loads(cleaned_text)
