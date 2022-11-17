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

	def test_get_set_of_all_cards(self):
		expected = set([
			C("R1"),C("R2"),C("R3"),C("R4"),C("R5"),
			C("W1"),C("W2"),C("W3"),C("W4"),C("W5"),
			C("B1"),C("B2"),C("B3"),C("B4"),C("B5"),
			C("G1"),C("G2"),C("G3"),C("G4"),C("G5"),
			C("Y1"),C("Y2"),C("Y3"),C("Y4"),C("Y5")])
		self.assertEqual(expected, Card.get_set_of_all_cards())

if __name__ == '__main__':
    unittest.main()