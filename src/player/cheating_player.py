from logic.player import Player
from logic.move import *

class CheatingPlayer(Player):
	def __init__(self, pid, player_count):
		super().__init__(pid)
		self.board = None
		self.player_count = player_count
	def is_cheater(self):
		return True
	def on_board_update(self, board):
		self.board = board

	def play(self):
		# Play if hand is playable
		hand = self.board.get_hands()[self.pid]
		for i in range(len(hand)):
			if self.board.is_playable(hand[i]):
				return Play(i)

		# Clue if clues are available to kill time
		# (as long as someone as something playable)
		if self.board.get_clue_count() > 0:
			return self.random_clue()
			someone_has_something_playable = False
			for i in range(self.player_count):
				other_hand = self.board.get_hands()[i]
				for c in other_hand:
					if self.board.is_playable(c):
						someone_has_something_playable = True
			if someone_has_something_playable:
				return self.random_clue()

		# Discard Trash, if possible
		for i in range(len(hand)):
			if self.board.is_trash(hand[i]):
				return Discard(i)

		# Discard non-danger cards, if possible
		danger_cards = self.board.get_danger_cards()
		for i in range(len(hand)):
			if hand[i] not in danger_cards:
				return Discard(i)
		# Discard a card
		return Discard(self.player_count-1)

	def random_clue(self):
		return self.board.get_random_valid_clue((self.pid+1)%self.player_count)
	
