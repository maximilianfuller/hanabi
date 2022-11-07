from logic.player import Player
from logic.move import *
from collections import Counter
from logic.runner import Runner


class CheatingPlayer(Player):
	def is_cheater(self):
		return True

	def play(self):
		# Play if hand is playable
		hand = self.board_view.get_hands()[self.pid]
		for i in range(len(hand)):
			if self.board_view.is_playable(hand[i]):
				return Play(i)

		# Clue if clues are available to kill time
		# (as long as someone has something playable)
		if self.board_view.get_clue_count() > 0:
			someone_has_something_playable = False
			for i in range(self.player_count):
				other_hand = self.board_view.get_hands()[i]
				for c in other_hand:
					if self.board_view.is_playable(c):
						someone_has_something_playable = True
			if someone_has_something_playable:
				return self.random_clue()

		# Discard Trash, if possible
		for i in range(len(hand)):
			if self.board_view.is_trash(hand[i]):
				return Discard(i)

		# Discard non-danger cards, if possible. Prefer cards that already appear multiple times in all hands, then prefer higher cards.
		danger_cards = self.board_view.get_danger_cards()
		all_visible_cards = []
		for i in range(self.player_count):
			all_visible_cards.extend(self.board_view.get_hands()[i])
		all_visible_card_counts = Counter(all_visible_cards)
		candidate_non_danger_indices = []
		for i in range(len(hand)):
			if hand[i] not in danger_cards:
				candidate_non_danger_indices.append(i)
		candidate_non_danger_indices.sort(key=lambda i: (100 if all_visible_card_counts[hand[i]] > 1 else 0) + hand[i].get_number().value)
		if candidate_non_danger_indices:
			return Discard(candidate_non_danger_indices[-1])

		# Discard the last card
		return Discard(len(hand)-1)

	def random_clue(self):
		return self.board_view.get_random_valid_clue((self.pid+1)%self.player_count)
	
