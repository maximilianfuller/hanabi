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
		hands[self.pid] = [None for _ in range(STARTING_CARDS_FOR_PLAYERS[self.num_players])]
		self.player_models = {i: PlayerModel(i, hands[i]) for i in range(self.num_players)}

	def on_board_update(self):
		board_hands = self.board_view.get_hands()
		for pid, model in self.player_models.items():
			model.process_update(self.board_view)

	def play(self):
		# Try to play
		playable_index = self.player_models[self.pid].get_playable_index(self.board_view)
		if playable_index >= 0:
			return Play(playable_index)

		# Otherwise try to clue
		if self.board_view.get_clue_count() > 0:
			#prefer to clue next player
			player_rotation = [i%self.num_players for i in range(self.pid+1, self.num_players+self.pid)]
			# Clue playable cards
			for i in player_rotation:
				clue = self.player_models[i].find_new_play_clue_to_give(self.board_view, self.get_known_and_clued_cards())
				if clue:
					return clue
			# Clue fives
			for i in player_rotation:
				clue = self.player_models[i].find_new_five_clue_to_give()
				if clue:
					return clue
			

		# Otherwise discard
		discard_index = self.player_models[self.pid].get_discard_index(self.board_view)
		return Discard(discard_index)

	def get_known_and_clued_cards(self):
		already_clued_set = set()
		for i in range(self.num_players):
			already_clued_set.update(self.player_models[i].get_known_and_clued_cards())
		return already_clued_set

	def get_knowledge_debug_string(self):
		return self.player_models[self.pid].get_debug_string()