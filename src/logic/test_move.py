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

	
if __name__ == '__main__':
    unittest.main()