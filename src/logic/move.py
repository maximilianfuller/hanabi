from logic.card import *

class Clue:
	def __init__(self, color_or_number, card_indice_set, target_player_index):
		self._color = color_or_number if isinstance(color_or_number, Color) else None
		self._number = color_or_number if isinstance(color_or_number, Number) else None
		self._card_indice_set = card_indice_set.copy()
		self._target_player_index = target_player_index

	def get_color(self):
		return self._color

	def get_number(self):
		return self._number

	def get_card_indice_set(self):
		return self._card_indice_set

	def get_target_player_index(self):
		return self._target_player_index

	def __str__(self):
		color_or_number = self.get_color() if self.get_color() else self.get_number()
		return f"clues player {self._target_player_index} that {sorted(list(self._card_indice_set))} are {color_or_number}"

	def __eq__(self, other):
		return  (self.get_color() == other.get_color() and 
			self.get_number() == other.get_number() and 
			self.get_card_indice_set() == other.get_card_indice_set() and
			self.get_target_player_index() == other.get_target_player_index())

	def __hash__(self):
	    return hash((self.get_number(), self.get_color()))

	@staticmethod
	def get_clue_for_color(hand, color, target_player_index):
		card_indice_set = set([i for i in range(len(hand)) if hand[i].get_color() == color])
		if not card_indice_set:
			return None
		return Clue(color, card_indice_set, target_player_index)


	@staticmethod
	def get_clue_for_number(hand, number, target_player_index):
		card_indice_set = set([i for i in range(len(hand)) if hand[i].get_number() == number])
		if not card_indice_set:
			return None
		return Clue(number, card_indice_set, target_player_index)


class Play:
	def __init__(self, card_index):
		self._card_index = card_index
		self._card_played = None

	def get_card_index(self):
		return self._card_index

	# Second class data used for printing only
	def add_card(self, card):
		self.card_played = card

	def __str__(self):
		return f'plays {self.card_played if self.card_played else "card"} at index {self._card_index}'

class Discard:
	def __init__(self, card_index):
		self._card_index = card_index

	def get_card_index(self):
		return self._card_index

	# Second class data used for printing only
	def add_card(self, card):
		self.card_discarded = card

	def __str__(self):
		return f'discards {self.card_discarded if self.card_discarded else "card"} at index {self._card_index}'