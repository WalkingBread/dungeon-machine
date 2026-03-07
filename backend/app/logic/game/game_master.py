from logic.brain.game_master_brain import GameMasterBrain
from logic.brain.player_action_outcome import PlayerActionOutcome
from logic.game.character import PlayerCharacter
from logic.game.game import Game
from logic.game.game_event import DiceEvent, GameEvent
from logic.game.player_action import PlayerAction
from logic.game.player_input import PlayerDiceRollResponse, PlayerDiceRollRequest, PlayerInputResponse, \
    PlayerInputRequest
from logic.game.scene import Scene, PlayerActionSequence


class GameMaster:
    def __init__(self):
        self._game: Game = None
        self._story: list[Scene] = []
        self._brain = GameMasterBrain()
        self._player_actions: dict[str, PlayerAction] = {}

    @property
    def game(self):
        return self._game

    @property
    def story(self):
        return self._story

    @property
    def current_scene(self):
        return self._story[-1] if self._story else None

    def create_game(self, theme: str, players: list[PlayerCharacter]):
        self._game = Game(theme, players)

    def introduce_story(self):
        self._begin_new_scene()
        self.current_scene.add(self._brain.get_game_introduction())

    def start_next_scene(self) -> list[PlayerInputRequest]:
        scene_description_sequence, events = (
            self._brain.provide_scene_setting(self._story, self._game.capture_game_state()))
        self._begin_new_scene()
        self.current_scene.add(scene_description_sequence)

        engine_event_sequences = self._game.execute_events(events)
        self.current_scene.extend(engine_event_sequences)

        # we create player actions and send request to the player to fill in what they want to do
        input_requests: list[PlayerInputRequest] = []
        for player_char in self._game.player_characters:
            self._player_actions[player_char.name] = PlayerAction(player_char.name)
            input_requests.append(PlayerInputRequest(player_char.name, "what do you do?"))

        return input_requests

    def _begin_new_scene(self):
        """
        helper function for start_next_scene
        """
        self._story.append(Scene())

    def handle_new_actions(self, inputs: list[PlayerInputResponse]) \
            -> list[PlayerDiceRollRequest] | None:

        for response in inputs:
            self._player_actions[response.player_name].add_player_action(response.player_action)

        actions = list(self._player_actions.values())
        outcomes = self._brain.provide_player_actions_outcome(self._story,
                                                            actions, self._game.capture_game_state())

        dice_requests: list[PlayerDiceRollRequest] = []

        for outcome in outcomes:
            dice_event = self._handle_player_action_outcome(outcome)
            if dice_event:
                dice_requests.append(self._build_player_dice_request(dice_event))

        if dice_requests:
            return dice_requests
        else:
            return None

    def handle_player_dice_results(self, dice_rolls: list[PlayerDiceRollResponse]) \
            -> list[PlayerDiceRollRequest] | None:
        for dice_roll in dice_rolls:
            self.add_player_dice_roll_result(dice_roll)

        # now that we updated all the actions we have to get the description for the outcomes
        pending_actions = [
            action for action in self._player_actions.values()
            if not action.is_finished
        ]
        outcomes = self._brain.provide_player_actions_outcome(self._story,
                                                   pending_actions, self._game.capture_game_state())

        dice_requests: list[PlayerDiceRollRequest] = []

        for outcome in outcomes:
            dice_event = self._handle_player_action_outcome(outcome)
            if dice_event:
                dice_requests.append(self._build_player_dice_request(dice_event))

        if dice_requests:
            return dice_requests
        else:
            return None

    def add_player_dice_roll_result(self, dice_roll: PlayerDiceRollResponse):
        player = dice_roll.player_name
        dice_result = dice_roll.dice_result
        self._player_actions[player].add_result_to_dice_roll(dice_result)

    def _handle_player_action_outcome(self, outcome: PlayerActionOutcome) \
            -> DiceEvent | None:
        """ Probably the biggest heavy lifter right now, what it does:
            - handles the LLM returned object of PlayerActionOutcome
            - adds description to the user actions and their dice rolls
            - updates the state of player's action (adding dice rolls, resolving actions)
            - if players action is finished it adds its description as a sequence to the
                current scene
            - passes the engine events to the game engine to execute them and appends
                the sequences of those events to the current scene
            - returns the events which are "dice events" so that the orchestrator
                can handle them further
        """
        player = outcome.player_name
        action = self._player_actions[player]

        if action.last_dice_roll:
            action.add_roll_description(outcome.outcome_description)

        if outcome.is_final_outcome:
            action.add_final_description(outcome.outcome_description)
            self.current_scene.add(PlayerActionSequence(player_name=outcome.player_name,
                                                        content=outcome.outcome_description))
            engine_sequences = self._game.execute_events(outcome.game_events)
            self.current_scene.extend(engine_sequences)

            return None
        else:
            dice_event = next((e for e in outcome.game_events if isinstance(e, DiceEvent)), None)
            engine_events = [e for e in outcome.game_events if not isinstance(e, DiceEvent)]
            action.add_new_dice_roll(dice_event.statistic)

            engine_sequences = self._game.execute_events(engine_events)
            self.current_scene.extend(engine_sequences)

            return dice_event

    def _build_player_dice_request(self, dice_event: DiceEvent) -> PlayerDiceRollRequest:
        return PlayerDiceRollRequest(dice_event.player_name, dice_event.statistic)
