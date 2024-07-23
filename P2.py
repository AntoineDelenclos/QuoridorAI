import random
from PathfindingPlayer import *
from Strategy import *
class Player2AI:
    def __init__(self, chromosome):
        self.chromosome = chromosome
    def get_move(self, game):
        # legal_moves = game.get_legal_moves()
        # # print("P2",legal_moves)
        # start = game.player_positions.get('P2')
        # goals = [(4,i) for i in range(5)]
        # # goals = [(4,2)]
        # grid = [[0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0]]
        # walls = transformBoardToWallsTuple(game.board)
        # # print("WALLS :",walls)
        # path = bfs(start,goals,grid,walls)
        # move_input = input_to_reach_next(start,path[1])
        # # print("PATH",path)
        action = strategy(self.chromosome,2,game)
        print("action",action)
        if len(action) == 1:
            return((action,))
        elif len(action) == 3:
            return((action[0],action[1],action[2]))   