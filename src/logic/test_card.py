from logic.card import *
import unittest

class TestCard(unittest.TestCase):
	def test_color(self):
		self.assertEqual(Card(Color.RED, Number.FOUR).get_color(), Color.RED)

	def test_number(self):
		self.assertEqual(Card(Color.RED, Number.FOUR).get_number(), Number.FOUR)

	def test_equal(self):
		self.assertEqual(Card(Color.RED, Number.FOUR), Card(Color.RED, Number.FOUR))

if __name__ == '__main__':
    unittest.main()