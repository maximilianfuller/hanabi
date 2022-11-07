from logic.runner import Runner
from player.cheating_player import *
from player.play_player import *
from player.discard_player import *
from player.alpha_player import *

###############################
# Configurable Params
NUM_SIMULATIONS = 1
PLAYER_TO_TEST = AlphaPlayer
PRINT_BOARDS = False
NUM_PLAYERS = 3
###############################

score_sum = 0
win_count = 0
for i in range(NUM_SIMULATIONS):
	players = [PLAYER_TO_TEST(i, NUM_PLAYERS) for i in range(NUM_PLAYERS)]
	runner = Runner(players)
	score = runner.run(should_print_board=PRINT_BOARDS)
	score_sum += score
	if score == 25:
		win_count += 1
print(f'average game score: {score_sum/NUM_SIMULATIONS}')
print(f'average win rate: {win_count/NUM_SIMULATIONS}')