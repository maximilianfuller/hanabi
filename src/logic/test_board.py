from logic.deck import Deck
import unittest
from logic.card import *
from logic.board import Board
from logic.move import *

FIVES = [
	Card(Color.RED, Number.FIVE), 
	Card(Color.WHITE, Number.FIVE), 
	Card(Color.BLUE, Number.FIVE), 
	Card(Color.GREEN, Number.FIVE), 
	Card(Color.YELLOW, Number.FIVE)
]

class TestBoard(unittest.TestCase):
	def test_out_of_turns_condition(self):
		board = Board(Deck(), 3)
		# 35 discards in a row goes through the entire deck
		for i in range(35):
			self.assertFalse(board.is_game_over())
			self.assertTrue(board.process_move(Discard(0)))
		# 3 remaining turns ends the game
		for i in range(3):
			self.assertFalse(board.is_game_over())
			self.assertTrue(board.process_move(Discard(0)))
		self.assertTrue(board.is_game_over())
		self.assertEqual(board.get_score(), 0)

	def test_loss_condition(self):
		# This deck initially deals out high cards
		deck = Deck(cards=list(reversed(Deck.get_new_sorted_cards())))
		board = Board(deck, 3)
		self.assertFalse(board.is_game_over())
		self.assertTrue(board.process_move(Play(0)))
		self.assertFalse(board.is_game_over())
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

	def test_cant_clue_self_invalid_clue(self):
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

	def test_get_hand(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		self.assertEqual(board.get_hands()[0][0], Card(Color.RED, Number.ONE))

	def test_hide_hand(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		board.remove_hand(0)
		self.assertFalse(0 in board.get_hands())

	def test_is_playable(self):
		board = Board(Deck(), 3)
		self.assertTrue(board.is_playable(Card(Color.RED, Number.ONE)))
		self.assertTrue(board.is_playable(Card(Color.WHITE, Number.ONE)))
		self.assertTrue(board.is_playable(Card(Color.BLUE, Number.ONE)))
		self.assertTrue(board.is_playable(Card(Color.GREEN, Number.ONE)))
		self.assertTrue(board.is_playable(Card(Color.YELLOW, Number.ONE)))
		self.assertFalse(board.is_playable(Card(Color.RED, Number.TWO)))
		self.assertFalse(board.is_playable(Card(Color.WHITE, Number.TWO)))
		self.assertFalse(board.is_playable(Card(Color.BLUE, Number.THREE)))
		self.assertFalse(board.is_playable(Card(Color.GREEN, Number.FOUR)))
		self.assertFalse(board.is_playable(Card(Color.YELLOW, Number.FIVE)))

	def test_is_trash(self):
		board = Board(Deck(Deck.get_new_sorted_cards()), 2)
		# Play blue one
		self.assertTrue(board.process_move(Play(0)))
		self.assertTrue(board.is_trash(Card(Color.RED, Number.ONE)))
		self.assertFalse(board.is_trash(Card(Color.BLUE, Number.ONE)))

	def test_get_danger_cards_fives(self):
		board = Board(Deck(), 2)
		self.assertEqual(board.get_danger_cards(), set(FIVES))

	def test_get_danger_cards_ones_and_twos(self):
		# H0: R5, R4, R3, R2, R1
		# H1: Y4, Y4, R4, B1, B1
		# P0 always plays their last card, P1 always discards their last card.
		cards = [
			C("R5"),
			C("R4"),
			C("R3"),
			C("R2"),
			C("R1"),
			C("Y4"),
			C("Y4"),
			C("R4"),
			C("B1"),
			C("B1"),
		]
		# Add fillers so game doesn't end. This deck is invalid but this is for testing convenience.
		for i in range(100):
			cards.append(C("W5"))

		board = Board(Deck(cards), 2)
		self.assertTrue(board.process_move(Play(4)))
		self.assertTrue(board.process_move(Discard(4)))
		self.assertTrue(board.process_move(Play(4)))
		self.assertTrue(board.process_move(Discard(4)))
		dangers = set(FIVES)
		# blue one is in danger
		dangers.add(C("B1"))
		self.assertEqual(board.get_danger_cards(), dangers)

		self.assertTrue(board.process_move(Play(4)))
		self.assertTrue(board.process_move(Discard(4)))
		dangers = set(FIVES)
		# red four is also now in danger
		dangers.add(C("B1"))
		dangers.add(C("R4"))
		self.assertEqual(board.get_danger_cards(), dangers)

		self.assertTrue(board.process_move(Play(4)))
		self.assertTrue(board.process_move(Discard(4)))
		self.assertTrue(board.process_move(Play(4)))
		self.assertTrue(board.process_move(Discard(4)))
		# red four is played so no longer in danger, red five played so no longer in danger.
		# yellow fours and fives not in danger since case is hopeless
		dangers = set([C("W5"), C("B5"), C("G5"), C("B1")])
		self.assertEqual(board.get_danger_cards(), dangers)



if __name__ == '__main__':
    unittest.main()