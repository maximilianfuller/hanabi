from logic.move import *

# Model for keeping track what a player should know. The left most card (and only the left most) in a 'play' clue is meant to be played.
class PlayerModel():
	def __init__(self, pid, hand):
		self._pid = pid
		self._hand = [CardModel(c) for c in hand]

	def process_update(self, board_view, previous_oob_card):
		# new_draw will be None if this the player's model
		pid, move, new_draw, actioned_card, is_final_round = board_view.get_last_action()
		if not move:
			return
		if isinstance(move, Play):
			self._maybe_process_finessed_play(board_view, previous_oob_card)
			self._process_new_card(move.get_card_index(), new_draw, pid, is_final_round)
		elif isinstance(move, Discard):
			self._process_new_card(move.get_card_index(), new_draw, pid, is_final_round)
		elif isinstance(move, Clue):
			self._maybe_process_finesse_clue(move, board_view, pid)
			self._maybe_process_five_clue(move, board_view, pid)			
			self._maybe_process_direct_clue(move, board_view, pid)	
			self._remember_clue(move, pid)
			clued_on_trash = False
			for i in range(len(self._hand)):
				if self._hand[i].is_trash(board_view) and self._hand[i].directly_clued:
					clued_on_trash = True
					self._hand[i].directly_clued = False
			if clued_on_trash:
				danger_index = self._get_index_of_next_discard()
				self._hand[danger_index].is_danger = True

		# infer last five (cheap inference until more robust inference is built)
		unfinished_colors = [color for color, number in board_view.get_played_cards().items() if number != Number.FIVE]
		if len(unfinished_colors) == 1:
		        for m in self._hand:
		                if m.public_card_knowledge.number == Number.FIVE:
		                        m.public_card_knowledge.color = unfinished_colors[0]


		# self._maybe_infer_fives(board_view)
		
	def _maybe_process_finessed_play(self, board_view, previous_oob_card):
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

	def _process_new_card(self, removed_card_index, new_draw, pid, is_final_round):
		if self._pid == pid:
			del self._hand[removed_card_index]
			if not is_final_round:
				# insert None new draws for unknown hands
				self._hand.insert(0, CardModel(new_draw))

	def _maybe_process_five_clue(self, clue, board_view, pid):
		if self._pid != clue.get_target_player_index():
			return
		if clue.get_number() == Number.FIVE:
			# Remember not to discard fives
			for j in clue.get_card_indice_set():
				self._hand[j].is_danger = True

	def _maybe_process_direct_clue(self, clue, board_view, pid):
		if self._pid != clue.get_target_player_index():
			return
		elif clue.get_number() == Number.ONE:
			# Remember to play all the ones
			for i in clue.get_card_indice_set():
				self._hand[i].directly_clued = True 
		elif clue.get_number() != Number.FIVE:
			# Remember to play only the leftmost card
			leftmost = min(clue.get_card_indice_set())
			self._hand[leftmost].directly_clued = True

	def _maybe_process_finesse_clue(self, clue, board_view, pid):
		n = board_view.get_player_count()
		previous_player_issued_clue = self._pid == (pid+1)%n
		clue_was_for_next_player = self._pid == (clue.get_target_player_index()-1)%n
		if previous_player_issued_clue and clue_was_for_next_player:
			target_index = min(clue.get_card_indice_set())
			hands = board_view.get_hands()
			# The clued player is unaware of the finesse--they cannot be notified
			if clue.get_target_player_index() in hands:
				target_card = board_view.get_hands()[clue.get_target_player_index()][target_index]
				# Must be two plus the board
				played_cards = board_view.get_played_cards()
				number_on_board = played_cards[target_card.get_color()]
				board_value = number_on_board.value if number_on_board else 0
				if board_value+2 != target_card.get_number().value:
					return
				# Don't conflate with a five clue
				if clue.get_number() == Number.FIVE:
					return
				self._hand[0].is_finessed = True

	def _remember_clue(self, clue, pid):
		if self._pid != clue.get_target_player_index():
			return
		for i in clue.get_card_indice_set():
			if clue.get_color():
				self._hand[i].public_card_knowledge.color = clue.get_color()
			else:
				self._hand[i].public_card_knowledge.number = clue.get_number()


	def _get_cards(self):
		return [m.card for m in self._hand]

	# def _maybe_infer_fives(self, board_view):
	# 	for model in self._hand:
	# 		if model.public_card_knowledge.number == Number.FIVE and not model.public_card_knowledge.maybe_get_card():
	# 			possible_cards = model.infer_card_set_from_visible_cards(board_view)
	# 			if len(possible_cards) == 1:
	# 				i 


	# Gets a play clue that hasn't already been clued. If there are none, returns None.
	def find_new_play_clue_to_give(self, board_view, known_and_clued_cards):
		for i in range(len(self._hand)-1, -1, -1):
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
							return Clue.get_clue_for_number(self._get_cards(), number, self._pid)

				# Try to clue color.
				clue = Clue.maybe_get_color_clue_if_left_most(self._get_cards(), i, self._pid)
				if clue:
					return clue

				# Cluing fives is reserved for a five clue, not a play clue
				elif number != Number.FIVE and number != Number.ONE:
					clue = Clue.maybe_get_number_clue_if_left_most(self._get_cards(), i, self._pid)
					if clue:
						return clue

				
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
		# This card can't be finessed
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
				is_bluff = color != first_card_of_next_player.get_color()
				clue = Clue.maybe_get_color_clue_if_left_most(hand, i, last_player)
				if clue: 
					return clue
				# bluffs can't clue number	
				if not is_bluff:
					# Giving a FIVE clue is reserved as a danger clues
					if first_card_of_next_player.get_number() != Number.FOUR:
						clue = Clue.maybe_get_number_clue_if_left_most(hand, i, last_player)
						if clue: 
							return clue

	# Gets a five clue that hasn't already been clued. If there are none, returns None.
	def find_new_five_clue_to_give(self, clue_last_n, board_view):
		index = self.get_discard_index(board_view)
		for i in range(index, index-clue_last_n, -1):
			model = self._hand[i]
			if model.is_danger:
				continue
			if model.card.get_number() != Number.FIVE:
				continue

			return Clue.get_clue_for_number(self._get_cards(), Number.FIVE, self._pid)
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
			if self._hand[i].is_trash(board_view):
				return i
		for i in range(len(self._hand)-1, -1, -1):
			if self._hand[i].is_danger:
				continue
			# if we know what the card is and its not trash, don't discard it.
			if self._hand[i].public_card_knowledge.maybe_get_card():
				continue
			return i
		return len(self._hand)-1

	def is_danger_card(self, index):
		return self._hand[index].is_danger

	# Clue ones if this player is unwaware of a non 5, non playable danger card
	def find_danger_clue(self, board_view):
		# If not all ones are played, a distraction clue of ones won't work.
		for col, num in board_view.get_played_cards().items():
			if not num:
				return None
		danger_index = self._get_index_of_next_discard()
		if danger_index < 0:
			return None
		card_to_discard = self._hand[danger_index].card
		if card_to_discard.get_number() == Number.FIVE:
			return None
		if board_view.is_playable(card_to_discard):
			return None
		if self._hand[danger_index].public_card_knowledge.maybe_get_card():
			return None
		if self._hand[danger_index].card in board_view.get_danger_cards():
			return Clue.get_clue_for_number(self._get_cards(), Number.ONE, self._pid)

	def _get_index_of_next_discard(self):
		for i in range(len(self._hand)-1, -1, -1):
			if self._hand[i].is_danger:
				continue
			return i
		return -1

	def get_known_and_clued_cards(self):
		out = set()
		out.update([m.card for m in self._hand if m.directly_clued])
		out.update([m.public_card_knowledge.maybe_get_card() for m in self._hand if m.public_card_knowledge.maybe_get_card()])
		return out

	def get_fully_known_five_colors(self):
		known_cards = [m.public_card_knowledge.maybe_get_card() for m in self._hand if m.public_card_knowledge.maybe_get_card()]
		return set([c.get_color() for c in known_cards if c.get_number == Number.FIVE])

	def get_debug_string(self):
		return str([str(m) for m in self._hand])


# Simple card model for tracking card playability and fives
class CardModel():
	def __init__(self, card):
		self.card = card
		self.directly_clued = False
		self.is_danger = False
		self.public_card_knowledge = CardKnowledge()
		self.private_card_knowledge = CardKnowledge()
		self.is_finessed=False

	# poor man's trash detection
	def is_trash(self, board_view):
		if board_view.is_trash(self.public_card_knowledge.maybe_get_card()):
			return True
		if self.public_card_knowledge.number == Number.ONE:
			for col, num in board_view.get_played_cards().items():
				if not num:
					return False
			return True
		return False

	# def infer_card_set_from_visible_cards(board_view):
	# 	visible_cards = board_view.get_played_and_discarded_cards()
	# 	for pid, cards in board_view.get_hands().items():
	# 		visible_cards.extend(cards)
	# 	visible_card_counter = Counter(visible_cards)
	# 	candidates = Card.get_set_of_all_cards()
	# 	color = self.public_card_knowledge.color
	# 	number = self.public_card_knowledge.number
	# 	candidates = set([c for c in candidates if c.get_color() == color])
	# 	candidates = set([c for c in candidates if c.get_number() == number])
	# 	candidates = set([c for c in candidates if visible_card_counter[c] < Deck.CARD_COUNTS[c.get_number()]])
	# 	return candidates

	def __str__(self):
		private_card = self.private_card_knowledge.maybe_get_card()
		private_card_knowledge_string = f'({private_card})' if private_card else ""
		return f'{self.public_card_knowledge}{private_card_knowledge_string}{"C" if self.directly_clued else ""}{"F" if self.is_finessed else ""}{"D" if self.is_danger else ""}'

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