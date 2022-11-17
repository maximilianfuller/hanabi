import unittest
from logic.player import Player
from logic.runner import Runner
from logic.move import *

class TestRunner(unittest.TestCase):
	class CheatingPlayer(Player):
		def __init__(self, pid, num_players):
			super().__init__(pid, num_players)
			self.play_count = 0
			self.update_count = 0
		def get_move(self):
			self.play_count += 1
			return Discard(0)
		def on_board_update(self):
			self.update_count += 1
			assert(self.pid not in self.board_view.get_hands())

	class HonestPlayer(Player):
		def __init__(self, pid, num_players):
			super().__init__(pid, num_players)
			self.play_count = 0
			self.update_count = 0
		def get_move(self):
			self.play_count += 1
			return Discard(0)
		def on_board_update(self):
			self.update_count += 1
			assert(self.pid in self.board_view.get_hands())
		def is_cheater(self):
			return True
		
	def test_runner(self):
		# Two honest, two cheaters.
		players = [TestRunner.HonestPlayer(i, 4) for i in range(2)]
		players.extend([TestRunner.CheatingPlayer(i+2, 4) for i in range(2)])

		runner = Runner(players)
		runner.run()
		# Deck has 50 - 16 = 34 cards, + 4 rounds after the deck is dry leaves 38 total plays.
		# We divide this up among the players.
		self.assertTrue(players[0].play_count == 10)
		self.assertTrue(players[1].play_count == 10)
		self.assertTrue(players[2].play_count == 9)
		self.assertTrue(players[3].play_count == 9)
		for i in range(4):
			self.assertTrue(players[i].update_count == 39)



if __name__ == '__main__':
    unittest.main()