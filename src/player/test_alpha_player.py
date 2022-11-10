from logic.card import *
from logic.board import BoardView
from player.alpha_player import AlphaPlayer
from logic.runner import *
import unittest


class TestAlphaPlayer(unittest.TestCase):
	def test_no_misplays(self):
		for i in range(100):
			players = [AlphaPlayer(i, 3) for i in range(3)]
			runner = Runner(players)
			runner.run()
			self.assertEqual(players[0].board_view.get_life_count(), 3)

	



if __name__ == '__main__':
    unittest.main()