from logic.move import *

# Model for keeping track what a player should know. The left most card in a clue is meant to be played.
class PlayerModel():
	# is_unknown_hand indicates whether the owner of the PlayerModel knows the contents of the hand
	# (i.e. it is their hand). We hard code the draw behavior for unknown cards.
	def __init__(self, pid, hand, is_unknown_hand=False):
		self._pid = pid
		self._hand = [CardModel(c) for c in hand]
		self._is_unknown_hand = is_unknown_hand

	def process_update(self, board_view):
		pid, move, new_draw = board_view.get_last_action()
		if not move:
			return
		if isinstance(move, Discard) or isinstance(move, Play):
			if self._pid == pid:
				del self._hand[move.get_card_index()]
				if self._is_unknown_hand:
					# Unknown hands always draw unknown cards.
					self._hand.insert(0, CardModel(None))
		else:
			if self._pid == move.get_target_player_index():
				leftmost = min(move.get_card_indice_set())
				self._hand[leftmost].should_play = True
		if self._pid == pid and new_draw:
			self._hand.insert(0, CardModel(new_draw))

	def get_hand(self):
		return [m.card for m in self._hand]

	# Gets a clue that hasn't already been clued. If there are none, returns None.
	def find_new_clue_to_give(self, board_view):
		for i in range(len(self._hand)):
			model = self._hand[i]
			if model.should_play:
				continue
			if board_view.is_playable(model.card):
				# Try to clue color. Since the clue is meant to target the left most card only, the 
				# clue won't work if there are cards of the same color to the left of the target card.
				color = model.card.get_color()
				if not [j for j in range(len(self._hand)) if j < i and self._hand[j].card.get_color() == color]:
					return Clue.get_clue_for_color(self.get_hand(), color, self._pid)
				# Try to clue number
				number = model.card.get_number()
				if not [j for j in range(len(self._hand)) if j < i and self._hand[j].card.get_number() == number]:
					return Clue.get_clue_for_number(self.get_hand(), number, self._pid)
		return None

	# gets the index of a card to play. -1 if there is none
	def get_playable_index(self):
		for i in range(len(self._hand)):
			if self._hand[i].should_play:
				return i
		return -1


# Simple card model for tracking card playability
class CardModel():
	def __init__(self, card):
		self.card = card
		self.should_play = False