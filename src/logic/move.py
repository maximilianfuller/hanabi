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

class Play:
	def __init__(self, card_index):
		self._card_index = card_index

	def get_card_index(self):
		return self._card_index

class Discard:
	def __init__(self, card_index):
		self._card_index = card_index

	def get_card_index(self):
		return self._card_index 


class ClueResult:
	def __init__(self, clue):
		self._clue = clue

	def get_clue(self):
		return self._clue

class PlayResult:
	def __init__(self, play, card, is_playable, new_card):
		self._play = play
		self._card = card
		self._is_playable = is_playable
		self._new_card = new_card

	def get_play(self):
		return self._play

	def get_card(self):
		return self._card

	def get_is_playable(self):
		return self._is_playable

	def get_new_card(self):
		return self._new_card

class DiscardResult:
	def __init__(self, discard, card, new_card):
		self._discard = discard
		self._card = card
		self._new_card = new_card

	def get_discard(self):
		return self._discard

	def get_card(self):
		return self._card

	def get_new_card(self):
		return self._new_card