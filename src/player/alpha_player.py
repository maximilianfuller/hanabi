from logic.player import Player
from logic.move import Play

# Simple player plays if they have a clue, otherwise clues if someone hasn't been clued, otherwise discards
class AlphaPlayer(Player):

	def __init__(self, pid, num_players):
		super().__init__(pid, num_players)

	def init_board_view(self, board_view):
		super().init_board_view(board_view)
		# Model everyone but yourself
		hands = self.board_view.get_hands()
		self.player_models = {i: PlayerModel(i, hands[i]) for i in range(self.num_players) if i != self.pid}

	def on_board_update(self):
		board_hands = self.board_view.get_hands()
		for pid, model in self.player_models.items():
			model.process_update(self.board_view)
			# Check to make sure model state matches board state
			assert(model.get_hand() == board_hands[pid])

	def play(self):
		return Play(0)




class CardModel():
	def __init__(self, card):
		self._card = card