from logic.move import *

# Model for keeping track what a player should know. The left most card (and only the left most) in a 'play' clue is meant to be played.
class PlayerModel():
	def __init__(self, pid, hand):
		self._pid = pid
		self._hand = [CardModel(c) for c in hand]

	def process_update(self, board_view, previous_oob_card):
		# new_draw will be None if this the player's model
		pid, move, new_draw, actioned_card, final_round = board_view.get_last_action()
		if not move:
			return
		if isinstance(move, Discard) or isinstance(move, Play):
			# Process Move/Play

			# TODO clean up
			# Process potential middle card play in a bluff
			if previous_oob_card:
				assert(board_view.get_player_count() > 2)
				_, prev_clue, _, _, _ = board_view.get_second_to_last_action()
				assert(isinstance(prev_clue, Clue))
				if prev_clue.get_target_player_index() == self._pid:
					leftmost = min(prev_clue.get_card_indice_set())
					is_finesse = prev_clue.get_number() or prev_clue.get_color() == previous_oob_card.get_color()
					if not is_finesse:
						# this was a bluff not a clue! Don't play this card
						self._hand[leftmost].directly_clued = False
						# Now we know what this card is
						ck = self._hand[leftmost].public_card_knowledge
						played_num = board_view.get_played_cards()[prev_clue.get_color()]
						played_num_val = played_num.value if played_num else 0
						ck.number = Number(played_num_val+2)


			if self._pid == pid:
				del self._hand[move.get_card_index()]
				if not final_round:
					# insert None new draws for unknown hands
					self._hand.insert(0, CardModel(new_draw))
		else:
			# handle clue

			# Handle Finessed cards
			n = board_view.get_player_count()
			previous_player_issued_clue = self._pid == (pid+1)%n
			clue_was_for_next_player = self._pid == (move.get_target_player_index()-1)%n
			if previous_player_issued_clue and clue_was_for_next_player:
				target_index = min(move.get_card_indice_set())
				hands = board_view.get_hands()
				# The clued player is unaware of the finesse--they cannot be notified
				if move.get_target_player_index() in hands:
					target_card = board_view.get_hands()[move.get_target_player_index()][target_index]
					if not board_view.is_playable(target_card) and move.get_number() != Number.FIVE:
						self._hand[0].is_finessed = True


				# play left most card
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

	# Gets a finesse clue. If there are none, returns None.
	@staticmethod
	def find_new_bluff_or_finesse_clue_to_give(cluer_pid, board_view, known_and_clued_cards):
		if board_view.get_player_count() == 2:
			return None
		hands = board_view.get_hands()
		next_player = (cluer_pid + 1)%board_view.get_player_count()
		last_player = (cluer_pid + 2)%board_view.get_player_count()
		first_card_of_next_player = hands[next_player][0]
		if not board_view.is_playable(first_card_of_next_player):
			return None
		if first_card_of_next_player in known_and_clued_cards:
			return None
		# This clue was a five clue, not a finesse clue
		if first_card_of_next_player.get_number() == Number.FIVE:
			return None
		# look for 'the board +2' in the last player
		target_cards = [Card(color, Number(number.value+2 if number else 2)) for color, number in board_view.get_played_cards().items() if not number or number.value <= 3]
		target_cards = set([card for card in target_cards if card not in known_and_clued_cards])
		hand = hands[last_player]
		for i in range(len(hand)):
			card = hand[i]
			if card in target_cards:
				color = card.get_color()
				number = card.get_number()
				is_finesse = color == first_card_of_next_player.get_color()
				#TODO move out
				if not [j for j in range(len(hand)) if j < i and hand[j].get_color() == color]:
					return Clue.get_clue_for_color(hand, color, last_player)
				# bluffs can't clue number	
				if is_finesse:
					if not [j for j in range(len(hand)) if j < i and hand[j].get_number() == number]:
						return Clue.get_clue_for_number(hand, number, last_player)

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
		playable_indices = [i for i in range(len(self._hand)) if 
			self._hand[i].directly_clued or 
			self._hand[i].is_finessed or
			board_view.is_playable(self._hand[i].public_card_knowledge.maybe_get_card())]
		return playable_indices[0] if playable_indices else -1

	# Return whether or not there is normal reason to play the card at index playable_index
	def is_oob(self, playable_index, board_view):
		if playable_index < 0:
			return None
		model = self._hand[playable_index]
		out = not model.directly_clued and not model.public_card_knowledge.maybe_get_card()
		return out

	# gets the index of the next card to discard. Discards from the right and avoids fives, and discards trash cards if they are known.
	def get_discard_index(self, board_view):
		for i in range(len(self._hand)):
			if board_view.is_trash(self._hand[i].public_card_knowledge.maybe_get_card()):
				return i
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

	def get_debug_string(self):
		return str([str(m) for m in self._hand])


# Simple card model for tracking card playability and fives
class CardModel():
	def __init__(self, card):
		self.card = card
		self.directly_clued = False
		self.is_five = False
		self.public_card_knowledge = CardKnowledge()
		self.is_finessed=False

	def __str__(self):
		return f'{self.public_card_knowledge}{"C" if self.directly_clued else ""}{"F" if self.is_finessed else ""}'

# Color or number properties known about a card
class CardKnowledge():
	def __init__(self):
		self.color = None
		self.number = None

	def maybe_get_card(self):
		if self.color and self.number:
			return Card(self.color, self.number)

	def __str__(self):
		return f'({self.color.name[0] if self.color else ""}{self.number.value if self.number else ""})'