from game import *

player1 = HumanPlayer("Human Player")
player2 = RandomPlayer("Random Player")

g = Game([player1, player1])

g.play()