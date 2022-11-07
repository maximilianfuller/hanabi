from logic.card import *
from player.cheating_player import CheatingPlayer
from player.models.player_model import PlayerModel
from logic.runner import *
import unittest


class TestPlayerModel(unittest.TestCase):
	# use a cheating player since it is a simple ai that performs clues, discards and plays
	def test_full_game(self):
		num_player = 5
		players = [CheatingPlayerWithPlayerModel(i, num_player) for i in range(num_player)]
		runner = Runner(players)
		score = runner.run()


class CheatingPlayerWithPlayerModel(CheatingPlayer):
	def init_board_view(self, board_view):
		super().init_board_view(board_view)
		# Model everyone but yourself
		hands = self.board_view.get_hands()
		self.player_models = {i: PlayerModel(i, hands[i]) for i in range(self.num_players) if i != self.pid}

	def on_board_update(self):
		board_hands = self.board_view.get_hands()
		for pid, model in self.player_models.items():
			model.process_update(self.board_view)
			# Check to make sure model state matches board state
			assert(model.get_hand() == board_hands[pid])



if __name__ == '__main__':
    unittest.main()