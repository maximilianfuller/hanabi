from logic.player import Player
from logic.move import Discard

class DiscardPlayer(Player):
	def __init__(self, pid):
		super().__init__(pid)
	def play(self):
		return Discard(0)
	def on_board_update(self, board):
		pass
	def is_cheater(self):
		return True
