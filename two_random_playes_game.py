from game import *

player1 = RandomPlayer("Random Player 1")
player2 = RandomPlayer("Random Player 2")

g = Game([player1, player2])

g.play(verbose=True)