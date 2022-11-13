from logic.move import *
from logic.deck import Deck
from collections import Counter
import copy

STARTING_CARDS_FOR_PLAYERS = {2: 5, 3: 5, 4: 4, 5: 4}
STARTING_CLUES = 8
STARTING_LIVES = 3

class Board():
	def __init__(self, deck, player_count):
		self._deck = deck
		starting_hands = {i: [self._deck.draw() for _ in range(STARTING_CARDS_FOR_PLAYERS[player_count])] for i in range(player_count)}
		self._player_count = player_count

		self._clue_count = STARTING_CLUES
		self._life_count = STARTING_LIVES
		self._hands = starting_hands.copy()
		self._played_cards = {
			Color.RED: None, 
			Color.WHITE: None, 
			Color.BLUE: None, 
			Color.YELLOW: None, 
			Color.GREEN: None
		}
		self._curr_player = 0
		self._turns_remaining_after_dry_deck = player_count
		self._played_and_discarded_cards = []
		self._moves = []
		# list of draws, None if nothing was drawn for that turn
		self._draws = []

	# Returns True iff validation succeeds
	def process_move(self, move):
		if not self.__validate_move(move):
			return False
		if self._deck.is_empty():
			self._turns_remaining_after_dry_deck -= 1
		self.__update_state(move)
		return True

	def is_game_over(self):
		# win condition
		if set(self._played_cards.values()) == set([Number.FIVE]):
			return True

		# lose condition
		if self._life_count <= 0:
			return True

		# out of turns condition
		if self._turns_remaining_after_dry_deck <= 0:
			return True

		return False

	def get_player_count(self):
		return len(self._hands)

	def get_clue_count(self):
		return self._clue_count

	def get_score(self):
		return sum([c.value if c else 0 for c in self._played_cards.values()])

	def get_life_count(self):
		return self._life_count

	def get_hands(self):
		# should be deep copy, but for perforance reasons we just use copy.
		# return copy.deepcopy(self._hands)
		return self._hands.copy()

	# Returns a tuple (last_player_id, last_move, new_card_drawn), new_card_drawn may be None
	# if the last move was a clue, or if we are at the end of the game
	def get_last_action(self):
		if not self._moves:
			return (None, None, None)
		last_move = self._moves[-1]
		last_draw = self._draws[-1]
		last_pid = (self._curr_player-1)%self.get_player_count()
		return (last_pid, last_move, last_draw)

	# Useful for testing and cheating bots.
	def get_random_valid_clue(self, target_player_index):
		hand = self._hands[target_player_index]
		color = hand[0].get_color()
		matching_indices = set([i for i in range(len(hand)) if hand[i].get_color() == color])
		return Clue(color, matching_indices, target_player_index)

	def is_playable(self, card):
		if not card: 
			return False
		if not self._played_cards[card.get_color()]:
			return card.get_number() == Number.ONE
		return self._played_cards[card.get_color()].value + 1 == card.get_number().value
	
	# Returns whether or not a card can never be played in the future (and is thus no longer useful).
	def is_trash(self, card):
		if not card:
			return False
		if not self._played_cards[card.get_color()]:
			return False
		return self._played_cards[card.get_color()].value >= card.get_number().value

	# Returns the set of cards that if discarded would result in the game being unwinnable.
	def get_danger_cards(self):
		out = set()
		out.add(Card(Color.RED, Number.FIVE))
		out.add(Card(Color.WHITE, Number.FIVE))
		out.add(Card(Color.BLUE, Number.FIVE))
		out.add(Card(Color.YELLOW, Number.FIVE))
		out.add(Card(Color.GREEN, Number.FIVE))

		# Add candidate danger cards
		for c, count in Counter(self._played_and_discarded_cards).items():
			if c.get_number() == Number.ONE:
				if count == 2:
					out.add(c)
			elif c.get_number() != Number.FIVE:
				if count == 1:
					out.add(c)
		# Remove played cards, since these are safe.
		for color, number in self._played_cards.items():
			if not number:
				continue
			for i in range(1, number.value+1):
				c = Card(color, Number(i))
				if c in out:
					out.remove(c)
		# Remove hopeless cards
		normal_deck_dist = Counter(Deck.get_new_sorted_cards())
		for c, count in Counter(self._played_and_discarded_cards).items():
			played_number = self._played_cards[c.get_color()]
			is_played = played_number and played_number.value >= c.get_number().value
			is_exhausted = normal_deck_dist[c] == count
			if not is_played and is_exhausted:
				# Remove higher cards of the same color since they are hopeless
				for i in range(c.get_number().value, 6):
					hopeless_card = Card(c.get_color(), Number(i))
					if hopeless_card in out:
						out.remove(hopeless_card)
		return out

	# Returns the set of cards that can no longer be played and prohibit victory in the game
	def get_hopeless_cards(self):
		out = set()
		for c, count in Counter(self._played_and_discarded_cards).items():
			played_number = self._played_cards[c.get_color()]
			is_played = played_number and played_number.value >= c.get_number().value
			if is_played:
				continue
			if c.get_number() == Number.ONE:
				if count == 3:
					out.add(c)
			elif c.get_number() != Number.FIVE:
				if count == 2:
					out.add(c)
			else:
				if count == 1:
					out.add(c)
		return out

	def __validate_move(self, move):
		if not move:
			return False
		if isinstance(move, Clue):
			# check if we have a clue
			if self._clue_count <= 0:
				return False
			# check if we are not self cluing
			if self._curr_player == move.get_target_player_index():
				return False
			# check if target player exists
			if move.get_target_player_index() >= self._player_count:
				return False
			# Check clued cards are valid
			hand = self._hands[move.get_target_player_index()]
			matching_cards = set()
			if move.get_number():
				matching_cards = set([i for i in range(len(hand)) if hand[i].get_number() == move.get_number()])
			elif move.get_color():
				matching_cards = set([i for i in range(len(hand)) if hand[i].get_color() == move.get_color()])
			if not matching_cards or matching_cards != move.get_card_indice_set():
				return False
		if isinstance(move, Play):
			if len(self._hands[self._curr_player]) <= move.get_card_index() or move.get_card_index() < 0:
				return False
		if isinstance(move, Discard):
			if len(self._hands[self._curr_player]) <= move.get_card_index() or move.get_card_index() < 0:
				return False
		return True				

	def __update_state(self, move):
		new_card = None
		if isinstance(move, Clue):
			self._clue_count -= 1
		elif isinstance(move, Play):
			card = self._hands[self._curr_player][move.get_card_index()]
			self._played_and_discarded_cards.append(card)
			if self.is_playable(card):
				self._played_cards[card.get_color()] = card.get_number()
				if card.get_number() == Number.FIVE:
					self._clue_count = min(self._clue_count+1, STARTING_CLUES)
			else:
				self._life_count -= 1
			del self._hands[self._curr_player][move.get_card_index()]
			new_card = self._deck.draw()
			if new_card:
				self._hands[self._curr_player].insert(0, new_card)
		elif isinstance(move, Discard):
			card = self._hands[self._curr_player][move.get_card_index()]
			self._played_and_discarded_cards.append(card)
			self._clue_count = min(self._clue_count+1, STARTING_CLUES)
			del self._hands[self._curr_player][move.get_card_index()]
			new_card = self._deck.draw()
			if new_card:
				self._hands[self._curr_player].insert(0, new_card)
		self._curr_player = (self._curr_player + 1) % self._player_count
		self._moves.append(move)
		self._draws.append(new_card)
		
	def __str__(self):
		out = ""
		for i in range(self._player_count):
			if i in self._hands:
				out += f'Player {i}: {[str(c) for c in self._hands[i]]}\n'
		readable_played_cards = [str(Card(k, v)) for k, v in self._played_cards.items() if v]
		out += (
			f'Board: {readable_played_cards}\n'
		    f'Deck: {self._deck.count()}\n'
		    f'Clues: {self._clue_count}\n'
		    f'Lives: {self._life_count}\n'
		    f'Score: {self.get_score()}\n'
			f'Danger Cards: {[str(c) for c in self.get_danger_cards() if c.get_number() != Number.FIVE]}\n'
			f'Hopeless Cards: {[str(c) for c in self.get_hopeless_cards()]}'

		)
		return out

# Board wrapper that hides data from a player
class BoardView():
	def __init__(self, board, player_index, is_cheater):
		self._board = board
		self._pid = player_index
		self._is_cheater = is_cheater

	def get_hands(self):
		hands = self._board.get_hands()
		if not self._is_cheater:
			del hands[self._pid]
		return hands

	# Returns p
	def get_last_action(self):
		pid, move, card = self._board.get_last_action()
		# distinguish between dry deck and hiding card from player
		final_round = bool(move) and not bool(card)
		# print(f'final round {final_round} {move} {card}')
		if not self._is_cheater and self._pid == pid:
			card = None
		return (pid, move, card, final_round)

	def is_game_over(self):
		return self._board.is_game_over()

	def get_player_count(self):
		return self._board.get_player_count()

	def get_clue_count(self):
		return self._board.get_clue_count()

	def get_life_count(self):
		return self._board.get_life_count()

	def get_random_valid_clue(self, target_player_index):
		if not self._is_cheater and target_player_index == self._pid:
			return None
		return self._board.get_random_valid_clue(target_player_index)

	def is_playable(self, card):
		return self._board.is_playable(card)
	
	def is_trash(self, card):
		return self._board.is_trash(card)
		
	def get_danger_cards(self):
		return self._board.get_danger_cards()
		