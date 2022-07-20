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
		self.assertEqual(board.get_score(), 0)

	def test_loss_condition(self):
		# This deck initially deals out high cards
		deck = Deck(cards=list(reversed(Deck.get_new_sorted_cards())))
		board = Board(deck, 3)
		self.assertTrue(board.process_move(Play(0)))
		self.assertTrue(board.process_move(Play(0)))
		self.assertFalse(board.is_game_over())
		self.assertTrue(board.process_move(Play(0)))
		self.assertTrue(board.is_game_over())

	def test_win_condition(self):
		# Create a deck such that last card in every players hand is always playable.
		# Each player plays out a color.
		# Note that when we first deal out cards, we first deal out 4 cards to the first player,
		# 4 to the next, etc. Deck is invalid since it contains redundant filler cards, 
		# but this is ok for easy testing purposes
		cards = []
		for color_i in range(1, 6):
			for number_i in range(4, 0, -1):
					cards.append(Card(Color(color_i), Number(number_i)))
		# Add all fives that weren't dealt in the initial hand
		for color_i in range(1, 6):
			cards.append(Card(Color(color_i), Number.FIVE))
		# Add filler cards so the game doesn't end early
		for _ in range(25):
			cards.append(Card(Color(Color.BLUE), Number.FIVE))
		board = Board(Deck(cards), 5)
		for _ in range(25):
			self.assertFalse(board.is_game_over())
			self.assertTrue(board.process_move(Play(3)))
		self.assertTrue(board.is_game_over)
		self.assertEqual(board.get_score(), 25)

	def test_max_clues(self):
		board = Board(Deck(), 3)
		for i in range(10):
			self.assertTrue(board.process_move(Discard(0)))
		self.assertEqual(board.get_clue_count(), 8)

	def test_no_clues_remaining_invalid_move(self):
		# Each player is dealt all ones
		deck = Deck(cards=Deck.get_new_sorted_cards())
		board = Board(deck, 2)

		for i in range(8):
			player_to_clue = (i+1)%2
			self.assertTrue(board.process_move(board.get_random_valid_clue(player_to_clue)))

		self.assertFalse(board.process_move(Clue(Number.ONE, set(range(1, 6)), 0)))

	def test_two_players(self):
		deck = Deck()
		board = Board(deck, 2)
		self.assertEqual(deck.count(), 40)

	def test_three_players(self):
		deck = Deck()
		board = Board(deck, 3)
		self.assertEqual(deck.count(), 35)

	def test_four_players(self):
		deck = Deck()
		board = Board(deck, 4)
		self.assertEqual(deck.count(), 34)

	def test_five_players(self):
		deck = Deck()
		board = Board(deck, 5)
		self.assertEqual(deck.count(), 30)

	def test_cant_clue_self_invalid_move(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		# player 0 is first player, can't clue self
		# note: among dealt sorted cards, first 3 cards are red
		self.assertFalse(board.process_move(Clue(Color.RED, set([0,1,2]), 0)))

	def test_non_existent_target_invalid_clue(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		# player index 429 does not exist
		self.assertFalse(board.process_move(Clue(Color.WHITE, set([0]), 429)))

	def test_empty_clue_invalid(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		# Note: player 1 has no green
		self.assertFalse(board.process_move(Clue(Color.GREEN, set(), 1)))

	def test_bad_color_invalid_clue(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		# first player does something random, like discard
		self.assertTrue(board.process_move(Discard(0)))
		# player 1 clues player 0
		# player 0 should have: [(R, 1), (R,1), (R,1), (W,1), (W,1)]
		# Clue is actually invalid, since card 1 was not clued
		self.assertFalse(board.process_move(Clue(Color.RED, set([0, 2]), 0)))

	def test_bad_number_invalid_clue(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		# first player does something random, like discard
		self.assertTrue(board.process_move(Discard(0)))
		# player 1 clues player 0
		# player 0 should have: [(R, 1), (R,1), (R,1), (W,1), (W,1)]
		# Clue is actually invalid, since card 4 should not be clued
		self.assertFalse(board.process_move(Clue(Number.ONE, set([0, 1, 2, 4]), 0)))

	def test_bad_index_invalid_play(self):
		board = Board(Deck(), 4)
		self.assertFalse(board.process_move(Play(419191)))

	def test_bad_index_invalid_dicard(self):
		board = Board(Deck(), 4)
		self.assertFalse(board.process_move(Discard(-1)))


if __name__ == '__main__':
    unittest.main()