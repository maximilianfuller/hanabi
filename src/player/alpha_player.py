from logic.player import Player
from logic.move import Play
from logic.board import *
from player.models.player_model import PlayerModel

# Simple player plays if they have a clue, otherwise clues if someone hasn't been clued, otherwise discards
class AlphaPlayer(Player):

	def __init__(self, pid, num_players):
		super().__init__(pid, num_players)

	def init_board_view(self, board_view):
		super().init_board_view(board_view)
		hands = self.board_view.get_hands()
		# Populate unknown self hand with Nones, we can still use a player model.
		hands[self.pid] = [None for _ in range(STARTING_CARDS_FOR_PLAYERS[self.num_players])]
		self.player_models = {i: PlayerModel(i, hands[i], is_unknown_hand=i==self.pid) for i in range(self.num_players)}

	def on_board_update(self):
		board_hands = self.board_view.get_hands()
		for pid, model in self.player_models.items():
			model.process_update(self.board_view)

	def play(self):
		# Try to play
		playable_index = self.player_models[self.pid].get_playable_index()
		if playable_index >= 0:
			return Play(playable_index)

		# Otherwise try to clue
		if self.board_view.get_clue_count() > 0:
			for i in range(self.num_players):
				if i == self.pid:
					continue
				clue = self.player_models[i].find_new_clue_to_give(self.board_view)
				if clue:
					return clue


		# Otherwise discard
		return Discard(STARTING_CARDS_FOR_PLAYERS[self.num_players]-1)


class CardModel():
	def __init__(self, card):
		self._card = card