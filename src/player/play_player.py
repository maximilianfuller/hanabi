from logic.player import Player
from logic.move import Play

class PlayPlayer(Player):
	def __init__(self, pid):
		super().__init__(pid)
	def play(self):
		return Play(0)
	def on_board_update(self, board):
		pass
