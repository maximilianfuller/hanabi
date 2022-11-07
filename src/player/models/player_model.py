from logic.move import *

# Model for keeping track what a player should know. The left most card in a clue is meant to be played.
class PlayerModel():
	def __init__(self, pid, hand):
		self._pid = pid
		self._hand = [CardModel(c) for c in hand]

	def process_update(self, board_view):
		pid, move, new_draw = board_view.get_last_action()
		if not move:
			return
		if isinstance(move, Discard) or isinstance(move, Play):
			if self._pid == pid:
				del self._hand[move.get_card_index()]
		else:
			if self._pid == move.get_target_player_index():
				leftmost = min(move.get_card_indice_set())
				self._hand[leftmost].should_play = True
		if self._pid == pid and new_draw:
			self._hand.insert(0, CardModel(new_draw))

	def get_hand(self):
		return [m.card for m in self._hand]

	# Gets a clue that hasn't already been clued. If there are none, returns None.
	def get_new_clue(self, board_view):
		for i in range(len(self._hand)):
			model = self.hand[i].model
			if model.should_play:
				continue
			if board_view.is_playable(model.card):
				# Try to clue color. Since the clue is meant to target the left most card only, the 
				# clue won't work if there are cards of the same color to the left of the target card.
				if not [m for m in self._hand if m.card.get_color() == model.card.get_color()]:
					return Clue.get_clue_for_color(self.get_hand(), m.card.get_color(), self._pid)
				# Try to clue number
				if not [m for m in self._hand if m.card.get_number() == model.card.get_number()]:
					return Clue.get_clue_for_number(self.get_hand(), m.card.get_number(), self._pid)
		return None





# Simple card model for tracking card playability
class CardModel():
	def __init__(self, card):
		self.card = card
		self.should_play = False