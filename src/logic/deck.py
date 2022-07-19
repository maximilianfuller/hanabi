from logic.card import *
import random

CARD_COUNTS = {Number.ONE:3, Number.TWO: 2, Number.THREE: 2, Number.FOUR: 2, Number.FIVE: 1}

class Deck:
	# Optional list of cards argument for testing
	def __init__(self, cards=None):
		if not cards:
			cards = Deck.get_new_sorted_cards()
			random.shuffle(cards)
		self._cards = cards

	def draw(self):
		if not self._cards:
			return None
			print(self._cards)
		return self._cards.pop()

	def is_empty(self):
		return not bool(self._cards)

	def count(self):
		return len(self._cards)

	@staticmethod
	def get_new_sorted_cards():
		cards = []
		for number in [Number(i) for i in range(5, 0, -1)]:
			for color in [Color(i) for i in range(1, 6)]:
				for _ in range(CARD_COUNTS[number]):
					cards.append(Card(color, number))
		return cards


