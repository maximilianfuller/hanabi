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

class Play:
	def __init__(self, card_index):
		self._card_index = card_index

	def get_card_index(self):
		return self._card_index

	def __str__(self):
		return f"plays card at index {self._card_index}"

class Discard:
	def __init__(self, card_index):
		self._card_index = card_index

	def get_card_index(self):
		return self._card_index 

	def __str__(self):
		return f"discards card at index {self._card_index}"