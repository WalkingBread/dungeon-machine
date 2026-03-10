import logging

import pytest

from logic.brain.modelmanager.v2.chains import Node, build_chain_registry
from logic.brain.modelmanager.v2.response_models import ActionDecision, RollRequirement, RollConsequence, FinalSummary
from genai.models import get_gpt_five_mini


chain_registry = build_chain_registry(get_gpt_five_mini())

@pytest.mark.llm
def test_decider_chain():
    """
    Test the DECIDER node to ensure it returns an ActionDecision.
    """
    node_type = Node.DECIDER
    chain = chain_registry[node_type]
    
    test_payload = {
        "scene": "A crowded market square with merchants shouting.",
        "intent": "I look around for a blacksmith.",
        "action_history": ""
    }
    
    logging.info(f"--- Testing Node: {node_type.name} ---")
    response = chain.invoke(test_payload)
    logging.info(f"Response: {response}")
    
    assert response is not None
    assert isinstance(response, ActionDecision)
    assert response.decision in ["CONTINUE", "FINISH"]

@pytest.mark.llm
def test_roll_setter_chain():
    """
    Test the ROLL_SETTER node to ensure it returns a RollRequirement.
    """
    node_type = Node.ROLL_SETTER
    chain = chain_registry[node_type]
    
    test_payload = {
        "scene": "You are facing a locked wooden door.",
        "intent": "I try to kick the door open.",
        "action_history": ""
    }
    
    logging.info(f"--- Testing Node: {node_type.name} ---")
    response = chain.invoke(test_payload)
    logging.info(f"Response: {response}")
    
    assert response is not None
    assert isinstance(response, RollRequirement)
    assert isinstance(response.stat, str)
    assert len(response.intro) > 0

@pytest.mark.llm
def test_roll_outcome_chain():
    """
    Test the ROLL_OUTCOME node to ensure it returns a RollConsequence.
    Note: This node requires an extra 'result' variable in the input.
    """
    node_type = Node.ROLL_OUTCOME
    chain = chain_registry[node_type]
    
    test_payload = {
        "scene": "You kicked the wooden door.",
        "intent": "I try to kick the door open.",
        "action_history": "Player decided to kick the door. Roll required: STRENGTH.",
        "result": "18 (Success)" # This is required by the prompt template
    }
    
    logging.info(f"--- Testing Node: {node_type.name} ---")
    response = chain.invoke(test_payload)
    logging.info(f"Response: {response}")
    
    assert response is not None
    assert isinstance(response, RollConsequence)
    assert isinstance(response.desc, str)
    assert len(response.desc) > 0

@pytest.mark.llm
def test_finalizer_chain_no_event():
    """
    Test the FINALIZER node to ensure it returns a FinalSummary.
    """
    node_type = Node.FINALIZER
    chain = chain_registry[node_type]
    
    test_payload = {
        "scene": "The door splinters and flies open.",
        "intent": "I try to kick the door open.",
        "action_history": "Player kicked the door. Roll: 18. Result: Success. The door broke open."
    }
    
    logging.info(f"--- Testing Node: {node_type.name} ---")
    response = chain.invoke(test_payload)
    logging.info(f"Response: {response}")
    
    assert response is not None
    assert isinstance(response, FinalSummary)
    assert isinstance(response.final_story, str)
    assert len(response.final_story) > 0

@pytest.mark.llm
def test_finalizer_chain_health_event():
    """
    Test the FINALIZER node to ensure it returns a FinalSummary with a health event.
    """
    node_type = Node.FINALIZER
    chain = chain_registry[node_type]

    test_payload = {
        "scene": "A group of rowdy, battle-scarred drunks are huddled around a circular table, shouting "
                 "over a game of cards.",
        "intent": "I draw my rusty dagger and try to leap onto their table to intimidate the whole lot of them.",
        "action_history": (
            "Player attempted an acrobatic intimidation attack. "
            "Roll: 1 (Critical Failure). "
            "Result: The player slipped on a puddle of spilled ale, crashed chin-first into the table edge, "
            "and accidentally stabbed their own thigh. The drunks are howling with laughter."
        )
    }

    logging.info(f"--- Testing Node: {node_type.name} ---")
    response = chain.invoke(test_payload)
    logging.info(f"Response: {response}")

    assert response is not None
    assert isinstance(response, FinalSummary)
    assert isinstance(response.final_story, str)
    assert len(response.final_story) > 0