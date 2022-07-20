from logic.move import *
from logic.card import *
import unittest

class TestMove(unittest.TestCase):
	def test_clue(self):
		clue = Clue(Color.BLUE, set([0, 3]), 2)
		self.assertEqual(clue.get_color(), Color.BLUE)
		self.assertEqual(clue.get_number(), None)
		self.assertEqual(clue.get_card_indice_set(), set([0, 3]))
		self.assertEqual(clue.get_target_player_index(), 2)

		clue = Clue(Number.THREE, set([0, 3]), 2)
		self.assertEqual(clue.get_color(),None)
		self.assertEqual(clue.get_number(), Number.THREE)
		self.assertEqual(clue.get_card_indice_set(), set([0, 3]))
		self.assertEqual(clue.get_target_player_index(), 2)

	def test_play(self):
		play = Play(2)
		self.assertEqual(play.get_card_index(), 2)

	def test_discard(self):
		discard = Discard(1)
		self.assertEqual(discard.get_card_index(), 1)

	def test_clue_result(self):
		clue = Clue(Color.BLUE, set([0, 3]), 2)
		clue_result = ClueResult(clue)
		self.assertEqual(clue_result.get_clue().get_color(), Color.BLUE)

	def test_play_result(self):
		play_result = PlayResult(
			Play(2), 
			Card(Color.GREEN, Number.FIVE), 
			False, 
			Card(Color.BLUE, Number.THREE))
		self.assertEqual(play_result.get_play().get_card_index(), 2)
		self.assertEqual(play_result.get_card().get_color(), Color.GREEN)
		self.assertEqual(play_result.get_is_playable(), False)
		self.assertEqual(play_result.get_new_card().get_color(), Color.BLUE)

	def test_discard_result(self):
		discard_result = DiscardResult(
			Discard(2), 
			Card(Color.GREEN, Number.FIVE), 
			Card(Color.BLUE, Number.THREE))
		self.assertEqual(discard_result.get_discard().get_card_index(), 2)
		self.assertEqual(discard_result.get_card().get_color(), Color.GREEN)
		self.assertEqual(discard_result.get_new_card().get_color(), Color.BLUE)

	
if __name__ == '__main__':
    unittest.main()