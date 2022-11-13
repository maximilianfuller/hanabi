from logic.board import *
from logic.deck import Deck
import copy

class Runner:
	def __init__(self, player_list):
		self._player_list = player_list
		self._board = Board(Deck(), len(self._player_list))

	def run(self, should_print_board=False):
		for i in range(len(self._player_list)):
			self._player_list[i].init_board_view(BoardView(self._board, i, self._player_list[i].is_cheater()))

		curr_player_index = 0
		move_number = 1
		self.__update_players()
		while not self._board.is_game_over():
			move = self._player_list[curr_player_index].play()
			if should_print_board:
				print(self._board)
				print()
				print('\n'.join([f'Player {i} knows {self._player_list[i].get_knowledge_debug_string()}' for i in range(len(self._player_list))]))
			prior_hand = self._board.get_hands()[curr_player_index].copy()
			if not self._board.process_move(move):
				raise Exception(f'player {curr_player_index} submitted invalid move: {move}')
			if should_print_board:
				player, move, new_draw = self._board.get_last_action()
				if not isinstance(move, Clue):
					move.add_card(prior_hand[move.get_card_index()])
				assert(player == curr_player_index)
				drawString = ""
				if new_draw:
					drawString = f' and draws {str(new_draw)}'
				print()
				print(f'MOVE NUMBER {move_number}')
				print(f'Player {curr_player_index} {move}{drawString}')
				print()
			self.__update_players()
			curr_player_index = (curr_player_index + 1)%len(self._player_list)
			move_number += 1
		if should_print_board:
			print(self._board)
		return self._board.get_score()

	def __update_players(self):
		for i in range(len(self._player_list)):
			self._player_list[i].on_board_update()