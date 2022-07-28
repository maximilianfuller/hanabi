import unittest
from logic.player import Player
from logic.runner import Runner
from logic.move import *

class TestRunner(unittest.TestCase):
	class CheatingPlayer(Player):
		def __init__(self, pid):
			super().__init__(pid)
		def play(self):
			return Discard(0)
		def on_board_update(self, board):
			self.assertTrue(self.pid not in board.get_hands())

	class HonestPlayer(Player):
		def __init__(self, pid):
			super().__init__(pid)
			self.play_count = 0
			self.update_count = 0
		def play(self):
			self.play_count += 1
			return Discard(0)
		def on_board_update(self, board):
			self.update_count += 1
			assert(self.pid in board.get_hands())
		def is_cheater(self):
			return True
		
	def test_runner(self):
		players = [TestRunner.HonestPlayer(i) for i in range(4)]
		runner = Runner(players)
		runner.run()
		self.assertTrue(players[0].play_count == 10)
		self.assertTrue(players[1].play_count == 10)
		self.assertTrue(players[2].play_count == 9)
		self.assertTrue(players[3].play_count == 9)



if __name__ == '__main__':
    unittest.main()