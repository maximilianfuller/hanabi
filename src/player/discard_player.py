from logic.player import Player
from logic.move import Discard

class DiscardPlayer(Player):
	def get_move(self):
		return Discard(0)