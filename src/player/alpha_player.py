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
		# check if move was out of the blue
		previous_oob_card = None
		pid, move, new_draw, actioned_card, final_round = self.board_view.get_last_action()
		if isinstance(move, Play):
			is_oob = self.player_models[pid].is_oob(move.get_card_index(), self.board_view)
			previous_oob_card = actioned_card if is_oob else None

		# update models as normal
		board_hands = self.board_view.get_hands()
		for pid, model in self.player_models.items():
			model.process_update(self.board_view, previous_oob_card)

	def get_move(self):
		# Try to play
		playable_index = self.player_models[self.pid].get_playable_index(self.board_view)
		if playable_index >= 0:
			return Play(playable_index)

		# Otherwise try to clue
		if self.board_view.get_clue_count() > 0:
			clue = PlayerModel.find_new_bluff_or_finesse_clue_to_give(self.pid, self.board_view, self.get_known_and_clued_cards())
			if clue:
				return clue
			#prefer to clue next player
			player_rotation = [i%self.num_players for i in range(self.pid+1, self.num_players+self.pid)]
			# Clue fives
			for i in player_rotation:
				clue = self.player_models[i].find_new_five_clue_to_give(1)
				if clue:
					return clue
			# Clue playable cards
			for i in player_rotation:
				clue = self.player_models[i].find_new_play_clue_to_give(self.board_view, self.get_known_and_clued_cards())
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

		return "\n".join([self.player_models[i].get_debug_string() for i in range(self.num_players)])