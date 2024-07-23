import random
from PathfindingPlayer import *
from Strategy import *

class Player1AI():
    def __init__(self, chromosome=None):
        self.chromosome = chromosome
    def get_move(self, game):
        action = strategy([1,8,1],1,game)
        # action = strategy(self.chromosome,1,game)
        if len(action) == 1:
            return((action,))
        elif len(action) == 3:
            return((action[0],action[1],action[2]))       