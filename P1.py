import random
from PathfindingPlayer import *

class Player1AI:    
    def get_move(self, game):
        legal_moves = game.get_legal_moves()
        #you can retrieve information from the game object
        # print("remaining walls",game.walls)
        # print("player_positions",game.player_positions)
        # print("board",game.board) 
        # ("P1",legal_moves)
        # print("P1 start",game.player_positions.get('P1'))
        start = game.player_positions.get('P1')
        goals = [(0,i) for i in range(5)]
        # goals = [(0,0)]
        grid = [[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]
        walls = transformBoardToWallsTuple(game.board)
        path = bfs(start,goals,grid,walls)
        move_input = input_to_reach_next(start,path[1])
        print("Start:",start)
        print("Goal:",goals)
        print("Walls:",walls)
        print("PATH",path)
        print("Move_input:",move_input)
        return((move_input,))
    
   #wallfun
    def place_wall(self, game, wall_type, row, col):
        """
        Attempt to place a wall for Player 1.
        return:
        bool: True if wall placed
        """
        # check walls left
        if game.walls['P1'] <= 0:
            return False
        
        # check coordo in valid range
        if row < 0 or row >= game.board_size - 1 or col < 0 or col >= game.board_size - 1:
            return False
        
        # if wall isn't offboard
        if (wall_type == 'H' and col == game.board_size - 2) or (wall_type == 'V' and row == game.board_size - 2):
            return False
        
        # if space taken by a wall
        if game.board[row][col] != False or game.board[row][col+1] != False or game.board[row+1][col] != False:
            return False
        
        # place it temp
        previous = game.update_board_wall((wall_type, row, col))
        
        # check if p1 and p2 can reach
        p1_can_reach = game.reachable(game.player_positions['P1'], (0, 0))
        p2_can_reach = game.reachable(game.player_positions['P2'], (game.board_size-1, 0))
        
        if not (p1_can_reach and p2_can_reach):
            # revert cuz those dumasses cannot reach
            game.restore_board_wall((wall_type, row, col), previous)
            return False
        
        # valid placement
        return True


       