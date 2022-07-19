from logic.deck import Deck
import unittest
from logic.card import *
from logic.board import Board
from logic.move import *

class TestBoard(unittest.TestCase):
	def test_out_of_turns_condition(self):
		board = Board(Deck(), 3)
		# 35 discards in a row goes through the entire deck
		for i in range(35):
			self.assertTrue(board.process_move(Discard(0)))
		self.assertFalse(board.is_game_over())
		# 3 remaining turns ends the game
		for i in range(3):
			self.assertTrue(board.process_move(Discard(0)))
		self.assertTrue(board.is_game_over())

	def test_loss_condition(self):
		pass

	def test_win_condition(self):
		pass

	def test_max_clues(self):
		board = Board(Deck(), 3)
		for i in range(10):
			self.assertTrue(board.process_move(Discard(0)))
		self.assertEqual(board.get_clue_count(), 8)

	def test_no_clues_remaining_invalid_move(self):
		# Each player is dealt all ones
		deck = Deck(cards=Deck.get_new_sorted_cards())
		board = Board(deck, 3)

		for i in range(8):
			player_to_clue = (i+1)%3
			# Clue the next person on all ones
			self.assertTrue(board.process_move(Clue(Number.ONE, set(range(1, 6)), player_to_clue)))

		self.assertFalse(board.process_move(Clue(Number.ONE, set(range(1, 6)), 0)))

	def test_cant_clue_self_invalid_move(self):
		pass

	def test_game_over_invalid_move(self):
		pass

	def test_bad_color_number_invalid_clue(self):
		pass

	def test_bad_index_invalid_clue(self):
		pass

	def test_bad_index_invalid_play(self):
		pass

	def test_bad_index_invalid_dicard(self):
		pass

	def test_get_score(self):
		pass

if __name__ == '__main__':
    unittest.main()