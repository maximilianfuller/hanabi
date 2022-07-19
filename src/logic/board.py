from move import *
from deck import Deck

STARTING_CARDS_FOR_PLAYERS = {2: 5, 3: 5, 4: 4, 5: 4}
STARTING_CLUES = 8
STARTING_LIVES = 3

class Board():
	def __init__(self, deck, player_count):
		self._deck = Deck()
		starting_hands = [[self._deck.draw() for _ in range(STARTING_CARDS_FOR_PLAYERS[player_count])] for _ in range(player_count)]
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

	# Returns True iff validation succeeds
	def process_move(self, move):
		if not self.__validate_move(move):
			return False
		move_result = self.__get_move_result(move)
		self.__update_state(move_result)
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

	def get_clue_count(self):
		return self._clue_count

	def __is_playable(self, card):
		if not self._played_cards[card.get_color()]:
			return card.get_number() == Number.ONE
		return self._played_cards[card.get_color()].value + 1 == card.get_number().value
	
	def __validate_move(self, move):
		#TODO
		return True

	def __get_move_result(self, move):
		move_result = None
		if isinstance(move, Clue):
			move_result = ClueResult(move)
		elif isinstance(move, PlayResult):
			card = self._hands[self._curr_player][move.get_card_index()]
			move_result = PlayResult(move, card, self.__is_playable(card), self._deck.draw())
		elif isinstance(move, Discard):
			card = self._hands[self._curr_player][move.get_card_index()]
			move_result = DiscardResult(move, card, self._deck.draw())
		return move_result

	def __remove_and_maybe_draw(card_index):
		del self._hands[_curr_player][card_index]
		new_card = self.deck.draw()
		if new_card:
			self._hands[_curr_player].insert(0, new_card)			

	def __update_state(self, move_result):
		if self._deck.is_empty():
			self._turns_remaining_after_dry_deck -= 1
		if isinstance(move_result, ClueResult):
			self._clue_count -= 1
		elif isinstance(move_result, PlayResult):
			card = move_result.get_card()
			if move_result.get_is_playable():
				self._played_cards[card.get_color()] = card.get_number()
				if card.get_number() == Number.FIVE:
					self._clue_count += 1
			else:
				self._life_count -= 1
			del self._hands[self._curr_player][move_result.get_play().get_card_index()]
			new_card = move_result.get_new_card()
			if new_card:
				self._hands[self._curr_player].insert(0, new_card)
		elif isinstance(move_result, DiscardResult):
			self._clue_count += 1
			del self._hands[self._curr_player][move_result.get_discard().get_card_index()]
			new_card = move_result.get_new_card()
			if new_card:
				self._hands[self._curr_player].insert(0, new_card)
		self._curr_player = (self._curr_player + 1) % self._player_count
		
	def __str__(self):
		out = ""
		for i in range(self._player_count):
			out += f'Player {i}: {[str(c) for c in self._hands[i]]}\n'
		out += (
		    f'Deck: {self._deck.count()}\n'
		    f'Clues: {self._clue_count}\n'
		    f'Lives: {self._life_count}'
		)
		return out
