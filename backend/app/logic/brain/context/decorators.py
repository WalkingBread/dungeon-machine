from functools import wraps

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