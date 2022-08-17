from logic.move import *

class Player:
	def __init__(self, pid, board_view):
		self.pid = pid
		self.board_view = board_view

	# Returns either a Play, Discard, or Clue. Called when it is the players turn to play.
	def play(self):
		pass

	# Void function. Called after every player's move.
	def on_board_update(self):
		pass

	# Override and return true to receive boards that contains this player's cards.
	def is_cheater(self):
		return False
