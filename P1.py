import random
from PathfindingPlayer import *
from Strategy import *

class Player1AI():
    def __init__(self, chromosome):
        self.chromosome = chromosome
    def get_move(self, game):
        # legal_moves = game.get_legal_moves()
        # #you can retrieve information from the game object
        # print("remaining walls",game.walls)
        # # print("player_positions",game.player_positions)
        # # print("board",game.board) 
        # # ("P1",legal_moves)
        # # print("P1 start",game.player_positions.get('P1'))
        # start = game.player_positions.get('P1')
        # goals = [(0,i) for i in range(5)]
        # # goals = [(0,0)]
        # grid = [[0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0]]
        # walls = transformBoardToWallsTuple(game.board)
        # path = bfs(start,goals,grid,walls)
        # move_input = input_to_reach_next(start,path[1])
        # print("Start:",start)
        # print("Goal:",goals)
        # print("Walls:",walls)
        # print("PATH",path)
        # print("Move_input:",move_input)

        # action = strategy([2,2,1],1,game)
        action = strategy(chromosome,1,game)
        return((action,))       