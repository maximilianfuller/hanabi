from logic.move import *

class Player:
	def __init__(self, pid):
		self.pid = pid

	# Returns either a Play, Discard, or Clue. Called when it is the players turn to play.
	def play(self):
		pass

	# Void function. Consumes a board. Called after every player's move.
	def on_board_update(self, board):
		pass

	# Override and return true to receive boards that contains this player's cards.
	def is_cheater(self):
		return False
