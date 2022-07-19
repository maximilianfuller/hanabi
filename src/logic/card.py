from enum import Enum

class Color(Enum):
	RED = 1
	WHITE = 2
	BLUE = 3
	YELLOW = 4
	GREEN = 5

class Number(Enum):
	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5

class Card:
	def __init__(self, color, number):
		assert(isinstance(color, Color))
		assert(isinstance(number, Number))
		self._color = color
		self._number = number

	def get_color(self):
		return self._color

	def get_number(self):
		return self._number

	def __hash__(self):
		return hash((self.get_color(), self.get_number()))

	def __eq__(self, other):
		return  self.get_color() == other.get_color() and self.get_number() == other.get_number()

	def __str__(self):
		return f'({self.get_color().name[0]},{self.get_number().value})'
