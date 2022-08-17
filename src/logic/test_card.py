from logic.card import *
import unittest
from logic.deck import *

class TestCard(unittest.TestCase):
	def test_color(self):
		self.assertEqual(Card(Color.RED, Number.FOUR).get_color(), Color.RED)

	def test_number(self):
		self.assertEqual(Card(Color.RED, Number.FOUR).get_number(), Number.FOUR)

	def test_equal(self):
		self.assertEqual(Card(Color.RED, Number.FOUR), Card(Color.RED, Number.FOUR))

	def test_helper_constuctor(self):
		for c in Deck.get_new_sorted_cards():
			self.assertEqual(c, C(f"{c.get_color().name[0]}{c.get_number().value}"))

if __name__ == '__main__':
    unittest.main()