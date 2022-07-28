from logic.move import *

class Player:
	def __init__(self, pid):
		self.pid = pid

	def play(self):
		pass

	def on_board_update(self, board):
		pass

	def is_cheater(self):
		return False
