from logic.player import Player
from logic.move import Play

class PlayPlayer(Player):
	def get_move(self):
		return Play(0)
