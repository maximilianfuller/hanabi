from logic.move import *

class Player:
	# pid is a number in [0, # of players), so this player can identify itself and its 
	# position relative to other players. player_count is the number of players
	def __init__(self, pid, player_count):
		self.pid = pid
		self.player_count = player_count

	# Called at init time to notify the player of the board view used during the entire game.
	def init_board_view(self, board_view):
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
