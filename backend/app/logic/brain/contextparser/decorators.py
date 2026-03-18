from functools import wraps

from logic.game.player_action import ActionVerificationException

# This module contains decorators used by context parser for verification

def require_player_context(func):
    """
    Decorator to ensure the PlayerAction object has a valid name and intent
    before proceeding with parsing for the LLM.
    """
    @wraps(func)
    def wrapper(self, action: 'PlayerAction', *args, **kwargs):

        if not action.player_name or not action.player_name.strip():
            raise ActionVerificationException("Player name is required for narrative context.")

        if not action.player_action or not action.player_action.strip():
            raise ActionVerificationException(
                f"Player '{action.player_name}' provided no action text."
            )

        if len(action.player_action.strip()) < 3:
            raise ActionVerificationException(
                f"Action '{action.player_action}' is too short for the engine to process."
            )

        return func(self, action, *args, **kwargs)

    return wrapper

class StoryVerificationException(Exception):
    """Raised when the story history is missing, empty, or malformed."""
    pass


def require_story_context(func):
    """
    Decorator to ensure the story list and the relevant scene
    are populated before processing.
    """
    @wraps(func)
    def wrapper(self, story, *args, **kwargs):
        if story is None:
            raise StoryVerificationException("Story context is None.")

        if not story:
            raise StoryVerificationException(
                "The story history is empty. No scenes found."
            )

        last_scene = story[-1]
        if len(last_scene) == 0:
            raise StoryVerificationException(
                f"The current scene (index {len(story)-1}) has no sequences. "
                "Context cannot be generated from an empty scene."
            )

        return func(self, story, *args, **kwargs)

    return wrapper