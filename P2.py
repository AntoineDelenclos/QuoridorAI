import random
from PathfindingPlayer import *

class Player2AI:
    def get_move(self, game):
        legal_moves = game.get_legal_moves()
        # print("P2",legal_moves)
        start = game.player_positions.get('P2')
        goals = [(4,i) for i in range(5)]
        grid = [[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]
        walls = transformBoardToWallsTuple(game.board)
        # print("WALLS :",walls)
        path = bfs(start,goals,grid,walls)
        move_input = input_to_reach_next(start,path[1])
        # print("PATH",path)
        return((move_input,))
