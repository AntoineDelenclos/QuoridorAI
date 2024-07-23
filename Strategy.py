import random
from PathfindingPlayer import *


#I need the grid and the walls
#When I have this I can then use pathfinding to calculate both how much squares we are to win (same for the opponent)
#How many walls does the opponent have and how many do I have

# def bestWallThatCanBePlaced(grid,)

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
            if len(legal_moves[0]) == 3:
                return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            elif len(legal_moves[0]) == 1:
                return None
    if nextMove == 'D':
        if ('H',start[0],start[1]) in legal_moves:
            return ('H',start[0],start[1])
        if ('H',start[0],start[1]-1) in legal_moves:
            return ('H',start[0],start[1]-1)
        if ('H',start[0],start[1]+1) in legal_moves:
            return ('H',start[0],start[1]+1)
        else:
            if len(legal_moves[0]) == 3:
                return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            elif len(legal_moves[0]) == 1:
                return None
    if nextMove == 'L':
        if ('V',end[0],end[1]) in legal_moves:
            return ('V',end[0],end[1])
        if ('V',end[0],end[1]-1) in legal_moves:
            return ('V',end[0],end[1]-1)
        if ('V',end[0],end[1]+1) in legal_moves:
            return ('V',end[0],end[1]+1)
        else:
            if len(legal_moves[0]) == 3:
                return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            elif len(legal_moves[0]) == 1:
                return None
    if nextMove == 'R':
        if ('V',start[0],start[1]) in legal_moves:
            return ('V',start[0],start[1])
        if ('V',start[0],start[1]-1) in legal_moves:
            return ('V',start[0],start[1]-1)
        if ('V',start[0],start[1]+1) in legal_moves:
            return ('V',start[0],start[1]+1)
        else:
            if len(legal_moves[0]) == 3:
                return (legal_moves[0][0],legal_moves[0][1],legal_moves[0][2])
            elif len(legal_moves[0]) == 1:
                return None
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

    numberOfPossibleOutputs = len(possibleOutput)

    if numberOfPossibleOutputs == 0:
        print("No possible output")
        if chromosome[4] == 0:
            finalOutput = "move"
        elif chromosome[4] == 1:
            finalOutput = "wall"
    if numberOfPossibleOutputs > 1:
        movePossible = False
        wallPossible = False
        for i in range(numberOfPossibleOutputs):
            if possibleOutput[i] == "move":
                movePossible = True
            if possibleOutput[i] == "wall":
                movePossible = True
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

    print("PATH P1 : ", pathP1)
    print("PATH P2 : ", pathP2)
    print("POSITION P1 : ", positionP1)
    print("POSITION P2 : ", positionP2)
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