from logic.move import *

class Player:
	# pid is a number in [0, num_players), so this player can identify itself and its 
	# position relative to other players.
	def __init__(self, pid, num_players):
		self.pid = pid
		self.num_players = num_players

	# Called at init time to notify the player of the board view used during the entire game.
	def init_board_view(self, board_view):
		self.board_view = board_view
		self.player_count = board_view.get_player_count()

	# Returns either a Play, Discard, or Clue. Called when it is the players turn to move.
	def get_move(self):
		pass

	# Void function. Called after every player's move.
	def on_board_update(self):
		pass

	# Override and return true to receive boards that contains this player's cards.
	def is_cheater(self):
		return False

	# Get string indicating what the player knows about their hand
	def get_knowledge_debug_string(self):
		return ""
