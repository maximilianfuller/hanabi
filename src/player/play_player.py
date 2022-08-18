from logic.player import Player
from logic.move import Play

class PlayPlayer(Player):
	def play(self):
		return Play(0)
