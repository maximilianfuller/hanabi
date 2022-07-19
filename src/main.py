from logic.runner import Runner
from player.play_player import *

NUM_SIMULATIONS = 10000

score_sum = 0
for i in range(NUM_SIMULATIONS):
	players = [PlayPlayer(i) for i in range(3)]
	runner = Runner(players)
	score = runner.run()
	score_sum += score
print(f'average game score with 3 players that play the first card: {score_sum/NUM_SIMULATIONS}')