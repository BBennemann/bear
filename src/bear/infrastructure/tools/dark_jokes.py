from langchain_core.tools import tool
import random

@tool
def dark_joke() -> str:
    """
    Fetches and returns a random dark humor joke.
    
    Use this tool strictly if the user asks for a dark humor or edgy joke. Returns the text directly.

    Args:
        None.

    Returns:
        str: The joke text.
    """

    jokes_list = [
        "Why don't vampires go to barbecues?... They don't like stakes.",
        "What's the difference between a snowman and a snowwoman?... Snowballs.",
        "I have a joke about time travel, but I'm not gonna share it. You guys didn't like it."
    ]
    return random.choice(jokes_list)
