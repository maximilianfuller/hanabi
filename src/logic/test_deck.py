from logic.deck import Deck
import unittest
from collections import defaultdict
from logic.card import *

class TestDeck(unittest.TestCase):
	def test_fifty_cards(self):
		deck = Deck()
		count = 0
		while deck.draw():
			count += 1
		self.assertEqual(count, 50)

	def test_empty_draw(self):
		deck = Deck()
		for i in range(50):
			deck.draw()

		self.assertEqual(deck.draw(), None)
		# still empty
		self.assertEqual(deck.draw(), None)

	def test_count(self):
		deck = Deck()
		self.assertEqual(deck.count(), 50)
		for i in range(31):
			deck.draw()
		self.assertEqual(deck.count(), 19)

	def test_is_empty(self):
		deck = Deck()
		self.assertFalse(deck.is_empty())
		for i in range(50):
			deck.draw()
		self.assertTrue(deck.is_empty())

	def test_distribution(self):
		deck = Deck()
		color_dist = defaultdict(int)
		number_dist = defaultdict(int)
		for i in range(50):
			card = deck.draw()
			number_dist[card.get_number()]+=1
			color_dist[card.get_color()]+=1
		self.assertEqual(set(color_dist.values()), set([10]))
		self.assertEqual(number_dist[Number.ONE], 15)
		self.assertEqual(number_dist[Number.TWO], 10)
		self.assertEqual(number_dist[Number.THREE], 10)
		self.assertEqual(number_dist[Number.FOUR], 10)
		self.assertEqual(number_dist[Number.FIVE], 5)

	def test_shuffled(self):
		first_cards = set()
		for i in range(100):
			deck = Deck()
			first_cards.add(deck.draw())
		self.assertGreater(len(first_cards), 1)


if __name__ == '__main__':
    unittest.main()