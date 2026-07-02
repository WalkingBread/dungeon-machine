from logic.game.character import PlayerCharacter

class TurnManager:
    def __init__(self, players: list[PlayerCharacter]):
        self._players = list(players)
        self._current_index = 0

    @property
    def round_finished(self) -> bool:
        return self._current_index >= len(self._players)

    @property
    def current_player(self) -> PlayerCharacter:
        if self.round_finished:
            return None

        return self._players[self._current_index]

    def next_player_turn(self) -> PlayerCharacter:
        if self.round_finished:
            return None
        
        player = self._players[self._current_index]
        self._current_index += 1
        return player

    def start_new_round(self) -> PlayerCharacter:
        self._current_index = 0
        return self.current_player
