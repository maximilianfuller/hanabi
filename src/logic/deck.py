from card import *
import random

CARD_COUNTS = {Number.ONE:3, Number.TWO: 2, Number.THREE: 2, Number.FOUR: 2, Number.FIVE: 1}

class Deck:
	def __init__(self):
		self._cards = []
		for number in [Number(i) for i in range(1, 6)]:
			for color in [Color(i) for i in range(1, 6)]:
				for _ in range(CARD_COUNTS[number]):
					self._cards.append(Card(color, number))
		random.shuffle(self._cards)

	def draw(self):
		if not self._cards:
			return None
		return self._cards.pop()

	def is_empty(self):
		return not bool(self._cards)

	def count(self):
		return len(self._cards)


