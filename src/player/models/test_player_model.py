from logic.card import *
from logic.board import BoardView
from player.cheating_player import CheatingPlayer
from player.models.player_model import PlayerModel
from logic.runner import *
import unittest


class TestPlayerModel(unittest.TestCase):
	# use a cheating player since it is a simple ai that performs clues, discards and plays
	def test_make_hands_align_over_full_game(self):
		num_player = 5
		players = [CheatingPlayerWithPlayerModel(i, num_player) for i in range(num_player)]
		runner = Runner(players)
		score = runner.run()

	def test_get_color_clue(self):
		mockBoardView = MockBoardView(C("B1"))
		model = PlayerModel(0,[C("R1"), C("B1"), C("B5")])
		self.assertEqual(model.find_new_play_clue_to_give(mockBoardView, set()), Clue(Color.BLUE, set([1, 2]), 0))

	def test_get_number_clue(self):
		mockBoardView = MockBoardView(C("R3"))
		model = PlayerModel(0,[C("R1"), C("R3"), C("B5")])
		self.assertEqual(model.find_new_play_clue_to_give(mockBoardView, set()), Clue(Number.THREE, set([1]), 0))

	def test_not_clueable(self):
		mockBoardView = MockBoardView(C("B5"))
		model = PlayerModel(0,[C("B1"), C("R5"), C("B5")])
		self.assertEqual(model.find_new_play_clue_to_give(mockBoardView, set()), None)		



class MockBoardView(BoardView):
	def __init__(self, playable_card):
		super().__init__(None, None, False)
		self.playable_card = playable_card

	def is_playable(self, card):
		return card == self.playable_card


class CheatingPlayerWithPlayerModel(CheatingPlayer):
	def init_board_view(self, board_view):
		super().init_board_view(board_view)
		hands = self.board_view.get_hands()
		self.player_models = {i: PlayerModel(i, hands[i]) for i in range(self.num_players)}

	def on_board_update(self):
		board_hands = self.board_view.get_hands()
		for pid, model in self.player_models.items():
			model.process_update(self.board_view)
			# Check to make sure model state matches board state
			assert(model.get_hand() == board_hands[pid])



if __name__ == '__main__':
    unittest.main()