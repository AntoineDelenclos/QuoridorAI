import random
# from PathfindingPlayer import *
# from Strategy import *
from collections import deque

def bfs(start, goals, grid, walls):
  """
  Performs Breadth-First Search to find a path from start to goal on a grid.

  Args:
    start: Starting position (tuple of (row, col)).
    goal: Goal position (tuple of (row, col)).
    grid: A 5x5 list of lists representing the grid. 1 indicates an obstacle, 0 is free.

  Returns:
    A list of tuples representing the path from start to goal, or None if no path exists.
  """
  paths = []

  for goal in goals:
    queue = deque([(start, [])])
    visited = set()

    while queue:
      (node, path) = queue.popleft()
      if node == goal:
        paths.append(path + [goal])
      if node not in visited:
        visited.add(node)
        for neighbor in get_neighbors(node, grid, walls):
          if neighbor not in visited:
            queue.append((neighbor, path + [node]))
  if len(paths) == 0:
    return None
  else:
    shortest = 0
    for i in range(len(paths)):
      if len(paths[i]) < len(paths[shortest]):
        shortest = i
    return paths[shortest]


def get_neighbors(node, grid, walls): #Returns valid neighbors of a node on the grid.
  neighbors = []
  row, col = node
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    r, c = row + dr, col + dc
    if 0 <= r < 5 and 0 <= c < 5 and grid[r][c] == 0:
        if not is_blocked_by_wall((row, col), (r, c), walls):
            neighbors.append((r, c))
  return neighbors

def is_blocked_by_wall(start, end, walls):
  sy, sx = start
  ey, ex = end
  x_min = min(sx,ex)
  y_min = min(sy,ey)
  if ex - sx == 1 or ex - sx == -1: #Vertical movement
    return ('V', y_min, x_min) in walls
  elif ey - sy == 1 or ey - sy == -1: #Horizontal movement
    return ('H', y_min, x_min) in walls
  else:
    return False

def input_to_reach_next(actual,next):
  move = (next[0]-actual[0],next[1]-actual[1])
  if move == (-1,0):
    return 'U'
  elif move == (1,0):
    return 'D'
  elif move == (0,-1):
    return 'L'
  elif move == (0,1):
    return 'R'
  else:
    return "Error"

def transformBoardToWallsTuple(board):
        wallsTuple = []
        for y in range(5):
            for x in range(5):
                if board[y][x] != False:
                    if board[y][x] == 'HH' or board[y][x] == 'H':
                      wallsTuple.append(('H',y,x))
                    elif board[y][x] == 'VV' or board[y][x] == 'V':
                      wallsTuple.append(('V',y,x))
                    elif board[y][x] == 'HV':
                      wallsTuple.append(('V',y,x))
                      wallsTuple.append(('H',y,x))
        return wallsTuple


#wallfunc
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

def score(player1Advantage, numberOfRemainingWalls, distanceToWin):
    score = player1Advantage * 3 + numberOfRemainingWalls * 4 + (2/distanceToWin) * 10
    return score

def whereToPlaceWall(start, end, legal_moves):
    nextMove = input_to_reach_next(start,end)
    if nextMove == 'U':
        if ('H',end[0],end[1]) in legal_moves:
            return ('H',end[0],end[1])
        elif ('H',end[0],end[1]-1) in legal_moves:
            return ('H',end[0],end[1]-1)
        elif ('H',end[0],end[1]+1) in legal_moves:
            return ('H',end[0],end[1]+1)
        else:
            return None
            # if len(legal_moves[0]) == 3:
            #     return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            # elif len(legal_moves[0]) == 1:
            #     return None
    if nextMove == 'D':
        if ('H',start[0],start[1]) in legal_moves:
            return ('H',start[0],start[1])
        if ('H',start[0],start[1]-1) in legal_moves:
            return ('H',start[0],start[1]-1)
        if ('H',start[0],start[1]+1) in legal_moves:
            return ('H',start[0],start[1]+1)
        else:
            return None
            # if len(legal_moves[0]) == 3:
            #     return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            # elif len(legal_moves[0]) == 1:
            #     return None
    if nextMove == 'L':
        if ('V',end[0],end[1]) in legal_moves:
            return ('V',end[0],end[1])
        if ('V',end[0],end[1]-1) in legal_moves:
            return ('V',end[0],end[1]-1)
        if ('V',end[0],end[1]+1) in legal_moves:
            return ('V',end[0],end[1]+1)
        else:
            return None
            # if len(legal_moves[0]) == 3:
            #     return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            # elif len(legal_moves[0]) == 1:
            #     return None
    if nextMove == 'R':
        if ('V',start[0],start[1]) in legal_moves:
            return ('V',start[0],start[1])
        if ('V',start[0],start[1]-1) in legal_moves:
            return ('V',start[0],start[1]-1)
        if ('V',start[0],start[1]+1) in legal_moves:
            return ('V',start[0],start[1]+1)
        else:
            return None
            # if len(legal_moves[0]) == 3:
            #     return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            # elif len(legal_moves[0]) == 1:
            #     return None
def strategy(chromosome, player, game):
    #Legal Moves
    legalMoves = game.get_legal_moves()
    #Grid / board
    grid = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
    #Walls on the board
    walls = transformBoardToWallsTuple(game.board)
    #Player1 advantage
    p1advantage = player == 1
    #Number of remaining walls for each player
    remainingP1Walls = game.walls.get('P1')
    remainingP2Walls = game.walls.get('P2')
    #Distance to win for both players
    positionP1 = game.player_positions.get('P1')
    positionP2 = game.player_positions.get('P2')
    goalsP1 = [(0,i) for i in range(5)]
    goalsP2 = [(4,i) for i in range(5)]
    pathP1 = bfs(positionP1, goalsP1, grid, walls)
    pathP2 = bfs(positionP2, goalsP2, grid, walls)
    distanceToWinP1 = len(pathP1) - 0
    distanceToWinP2 = len(pathP2) - 1
    #Scores
    scoreP1 = score(player1Advantage=True, numberOfRemainingWalls=remainingP1Walls, distanceToWin=distanceToWinP1)
    scoreP2 = score(player1Advantage=False, numberOfRemainingWalls=remainingP2Walls, distanceToWin=distanceToWinP2)
    
    #Chromosome impact
    possibleOutput = []

    if player == 1:
        Dist2WinXRatioHazardToLose = distanceToWinP1 * (int)(distanceToWinP1/distanceToWinP2)
        if len(pathP2) <= chromosome[0]:
            possibleOutput.append("wall")
        if chromosome[2] == 2:
            hypWall = whereToPlaceWall(positionP2,pathP2[1],legalMoves)
            if hypWall is not None:
                walls.append(hypWall)
                testPath = bfs(positionP2, goalsP2, grid, walls)
                if len(testPath) > distanceToWinP2:
                    possibleOutput.append("wall")
                walls.pop()
        if chromosome[3] <= scoreP2 - scoreP1:
            possibleOutput.append("wall")
    if player == 2:
        Dist2WinXRatioHazardToLose = distanceToWinP2* (int)(distanceToWinP2/distanceToWinP1)
        if len(pathP1) <= chromosome[0]:
            possibleOutput.append("wall")
        if chromosome[2] == 2:
            hypWall = whereToPlaceWall(positionP1,pathP1[1],legalMoves)
            if hypWall is not None:
                walls.append(whereToPlaceWall(positionP1,pathP1[1],legalMoves))
                testPath = bfs(positionP1, goalsP1, grid, walls)
                if len(testPath) > distanceToWinP1:
                    possibleOutput.append("wall")
                walls.pop()
        if chromosome[3] <= scoreP1 - scoreP2:
            possibleOutput.append("wall")
    
    if Dist2WinXRatioHazardToLose <= chromosome[1]:
        possibleOutput.append("move")

    if chromosome[2] == 1:
        possibleOutput.append("wall")

    if len(possibleOutput) == 0:
        finalOutput =  "move" #default action
    if len(possibleOutput) == 1:
        finalOutput = possibleOutput[0]
    if len(possibleOutput) > 1:
        movePossible = False
        wallPossible = False
        for i in range(len(possibleOutput)):
            if possibleOutput[i] == "move":
                movePossible = True
            if possibleOutput[i] == "wall":
                wallPossible = True
        if wallPossible and movePossible:
            if chromosome[4] == 0:
                finalOutput = "move"
            elif chromosome[4] == 1:
                finalOutput = "wall"
        else:
            if wallPossible:
                finalOutput = "wall"
            elif movePossible:
                finalOutput = "move"

    if finalOutput == "move" and player == 1:
        return input_to_reach_next(positionP1,pathP1[1])
    if finalOutput == "move" and player == 2:
        return input_to_reach_next(positionP2,pathP2[1])
    if finalOutput == "wall" and player == 1:
        if whereToPlaceWall(positionP2,pathP2[1],legalMoves) is None:
            return input_to_reach_next(positionP1,pathP1[1])
        else:
            return whereToPlaceWall(positionP2,pathP2[1],legalMoves)
    if finalOutput == "wall" and player == 2:
        if whereToPlaceWall(positionP1,pathP1[1],legalMoves) is None:
            return input_to_reach_next(positionP2,pathP2[1])
        else:
            return whereToPlaceWall(positionP1,pathP1[1],legalMoves)

class Player1AI():
    def __init__(self, chromosome=None):
        self.chromosome = chromosome
    def get_move(self, game):
        # action = strategy([19,45,1,8,1],1,game) #4,49,2 & [1,8,1]
        action = strategy(self.chromosome,1,game)
        if len(action) == 1:
            return((action,))
        elif len(action) == 3:
            return((action[0],action[1],action[2]))       