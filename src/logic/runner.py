from logic.board import Board
from logic.deck import Deck
import copy

class Runner:
	def __init__(self, player_list):
		self._player_list = player_list
		self._board = Board(Deck(), len(self._player_list))

	def run(self):
		curr_player_index = 0
		self.__update_players()
		while not self._board.is_game_over():
			move = self._player_list[curr_player_index].play()
			if not self._board.process_move(move):
				raise Exception("player submitted invalid move.")
			self.__update_players()
			curr_player_index = (curr_player_index + 1)%len(self._player_list)
		return self._board.get_score()

	def get_board_for_player(self, player_id):
		board = copy.copy(self._board)
		# Hide player's own hand
		if not self._player_list[player_id].is_cheater():
			board.remove_hand(player_id)
		return board

	def __update_players(self):
		for i in range(len(self._player_list)):
			self._player_list[i].on_board_update(self.get_board_for_player(i))