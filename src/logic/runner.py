from logic.board import Board
from logic.deck import Deck
import copy

class Runner:
	def __init__(self, player_list):
		self._player_list = player_list
		self._board = Board(Deck(), len(self._player_list))

	def run(self, should_print_board=False):
		curr_player_index = 0
		self.__update_players()
		while not self._board.is_game_over():

			move = self._player_list[curr_player_index].play()
			if should_print_board:
				print(self._board)
				print(f"Current Player: {curr_player_index}")
				print(move)
				print()
			if not self._board.process_move(move):
				raise Exception("player submitted invalid move.")
			self.__update_players()
			curr_player_index = (curr_player_index + 1)%len(self._player_list)
		if should_print_board:
			print(self._board)
		return self._board.get_score()

	def __update_players(self):
		for i in range(len(self._player_list)):
			self._player_list[i].on_board_update()