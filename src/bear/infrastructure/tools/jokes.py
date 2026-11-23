from langchain_core.tools import tool
import random

@tool
def joke() -> dict:
    """
    Fetches and returns a short, random joke.
    
    Use this tool when the user asks to tell a joke, something funny, or to brighten their day. The joke is returned in English.

    Args:
        None.

    Returns:
        dict: A dictionary containing the key "joke" with the joke text.
    """

    jokes_list = [
        "Why don't skeletons fight each other?... They don't have the guts.",
        "What do you call a fake noodle?... An impasta.",
        "Why did the scarecrow win an award?... Because he was outstanding in his field."
    ]
    return {"joke": random.choice(jokes_list)}