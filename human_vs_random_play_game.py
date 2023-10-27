from game import *

player1 = HumanPlayer("Human Player")
player2 = RandomPlayer("Random Player")

g = Game([player1, player2])

g.play(verbose=True)