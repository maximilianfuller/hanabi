# hanabi
Exploration of Hanabi AI using heuristics that I use when playing with friends.

Wins about 8% of the time with 3 players.

The main AI, AlphaPlayer:
* Clues other players on what to play (Only the leftmost card is meant to be played)
* Keeps track of all outstanding clues given by other players
* Clues other players on fives so they don't get discarded
* Clues finesses and bluffs when they are available
* Clues other players on ones (when all ones are already played) to indicate that they have a danger card in their discard slot
* Understands all the above clues
* Infers what color fives it has in its hand given that it sees fives in others' hands

There is certainly room for improvement in the middle game, as there are usually a couple of tough decisions on when to clue vs discard, or what order to prioritize clues in. Perhaps searching ahead to predict inevitible discards of danger cards could be a nice improvement. I usually win around 50% of games with friends, so this should be attainable.



There is also a CheatingPlayer that wins 98% of the time but can see their own hand.



To run, cd into src and run:
python main.py

(To print a single game, set PRINT_BOARD to true and NUM_SIMULATIONS to 1)



To run tests, cd into src and run:
python -m unittest

