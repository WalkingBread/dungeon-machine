import logging

from logic.game.scene import (
    Scene,
    GameIntroductionSequence,
    PlayerActionSequence,
    ActionDescriptionSequence
)


def test_scene_content_formatting():
    scene = Scene()

    scene.add(GameIntroductionSequence("The journey begins in a dark forest."))
    scene.add(PlayerActionSequence(content="I look around for tracks.", player_name="Valerius"))
    scene.add(ActionDescriptionSequence("You spot some heavy footprints near the stream."))

    content = scene.get_scene_content()
    logging.info(f"Scene content: {content}")
    lines = content.split("\n")
    assert len(lines) == 3
    assert lines[0] == "GameIntroduction: The journey begins in a dark forest."
    assert lines[1] == "PlayerAction - Valerius: I look around for tracks."
    assert lines[2] == "ActionDescription: You spot some heavy footprints near the stream."