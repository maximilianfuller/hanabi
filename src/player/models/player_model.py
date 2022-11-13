from logic.move import *

# Model for keeping track what a player should know. The left most card (and only the left most) in a 'play' clue is meant to be played.
class PlayerModel():
	def __init__(self, pid, hand):
		self._pid = pid
		self._hand = [CardModel(c) for c in hand]

	def process_update(self, board_view):
		# new_draw will be None if this the player's model
		pid, move, new_draw, final_round = board_view.get_last_action()
		if not move:
			return
		if isinstance(move, Discard) or isinstance(move, Play):
			# Process Move/Play
			if self._pid == pid:
				del self._hand[move.get_card_index()]
				if not final_round:
					# insert None new draws for unknown hands
					self._hand.insert(0, CardModel(new_draw))
		else:
			# Process clue
			if self._pid == move.get_target_player_index():
				if move.get_number() == Number.FIVE:
					# Remember not to discard fives
					for j in move.get_card_indice_set():
						self._hand[j].is_five = True
				elif move.get_number() == Number.ONE:
					# Remember to play all the ones
					for i in move.get_card_indice_set():
						self._hand[i].directly_clued = True 
				else:
					# Remember to play only the leftmost card
					leftmost = min(move.get_card_indice_set())
					self._hand[leftmost].directly_clued = True
				# Remember clue itself
				for i in move.get_card_indice_set():
					if move.get_color():
						self._hand[i].public_card_knowledge.color = move.get_color()
					else:
						self._hand[i].public_card_knowledge.number = move.get_number()

	def get_hand(self):
		return [m.card for m in self._hand]

	# Gets a play clue that hasn't already been clued. If there are none, returns None.
	def find_new_play_clue_to_give(self, board_view, known_and_clued_cards):
		for i in range(len(self._hand)):
			model = self._hand[i]
			if model.directly_clued:
				continue
			if board_view.is_playable(model.card) and not model.card in known_and_clued_cards:
				# Since the clue is meant to target the left most card only, the 
				# clue won't work if there are cards of the same type to the left of the target card.
				
				# Try to clue number
				number = model.card.get_number()

				# Try to clue multiple ones if none are already clued and all are playable. Cluing ones indicates to play all ones.
				if number == Number.ONE:
					ones = [m.card for m in self._hand if m.card.get_number() == number.ONE]
					if len(known_and_clued_cards.union(set(ones))) == len(known_and_clued_cards) + len(ones):
						if not [c for c in ones if not board_view.is_playable(c)]:
							return Clue.get_clue_for_number(self.get_hand(), number, self._pid)

				# Cluing fives is reserved for a five clue, not a play clue
				elif number != Number.FIVE:
					if not [j for j in range(len(self._hand)) if j < i and self._hand[j].card.get_number() == number]:
						return Clue.get_clue_for_number(self.get_hand(), number, self._pid)

				# Try to clue color.
				color = model.card.get_color()
				if not [j for j in range(len(self._hand)) if j < i and self._hand[j].card.get_color() == color]:
					return Clue.get_clue_for_color(self.get_hand(), color, self._pid)
		return None

	# Gets a five clue that hasn't already been clued. If there are none, returns None.
	def find_new_five_clue_to_give(self):
		for i in range(len(self._hand)-2, len(self._hand)):
			model = self._hand[i]
			if model.is_five:
				continue
			if model.card.get_number() != Number.FIVE:
				continue
			return Clue.get_clue_for_number(self.get_hand(), Number.FIVE, self._pid)
		return None

	# gets the index of a card to play. -1 if there is none
	def get_playable_index(self, board_view):
		for i in range(len(self._hand)):
			if self._hand[i].directly_clued:
				return i
			if board_view.is_playable(self._hand[i].public_card_knowledge.maybe_get_card()):
				return i
		return -1

	# gets the index of the next card to discard. Discards from the right and avoids fives, and discards trash cards if they are known.
	def get_discard_index(self, board_view):
		for i in range(len(self._hand)-1, -1, -1):
			if self._hand[i].is_five:
				continue
			return i

	def is_danger_card(self, index):
		return self._hand[index].is_five

	def get_known_and_clued_cards(self):
		out = set()
		out.update([m.card for m in self._hand if m.directly_clued])
		out.update([m.public_card_knowledge.maybe_get_card() for m in self._hand if m.public_card_knowledge.maybe_get_card()])
		return out


# Simple card model for tracking card playability and fives
class CardModel():
	def __init__(self, card):
		self.card = card
		self.directly_clued = False
		self.is_trash = False
		self.is_five = False
		self.public_card_knowledge = CardKnowledge()

	def __str__(self):
		return f'{self.card}, {self.directly_clued}, {self.is_five}, {self.public_card_knowledge}'

# Color or number properties known about a card
class CardKnowledge():
	def __init__(self):
		self.color = None
		self.number = None

	def maybe_get_card(self):
		if self.color and self.number:
			return Card(self.color, self.number)

	def __str__(self):
		return f'{self.color}, {self.number}'