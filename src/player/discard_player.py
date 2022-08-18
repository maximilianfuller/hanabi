from logic.player import Player
from logic.move import Discard

class DiscardPlayer(Player):
	def play(self):
		return Discard(0)