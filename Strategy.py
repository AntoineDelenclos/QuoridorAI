import random
from PathfindingPlayer import *


#I need the grid and the walls
#When I have this I can then use pathfinding to calculate both how much squares we are to win (same for the opponent)
#How many walls does the opponent have and how many do I have

# def bestWallThatCanBePlaced(grid,)

def score(player1Advantage, numberOfRemainingWalls, distanceToWin):
    score = player1Advantage * 3 + numberOfRemainingWalls * 4 + (2/distanceToWin) * 10
    return score

def whereToPlaceWall(start, end):
    nextMove = input_to_reach_next(start,end)
    if nextMove == 'U':
        #If wall is possible
        return ('H',end[0],end[1])
    if nextMove == 'D':
        return ('H',start[0],start[1])
    if nextMove == 'L':
        return ('V',end[0],end[1])
    if nextMove == 'R':
        return ('V',start[0],start[1])
    return None

def strategy(chromosome, player, game):
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
            walls.append(whereToPlaceWall(positionP2,pathP2[1]))
            testPath = bfs(positionP2, goalsP2, grid, walls)
            if len(testPath) > distanceToWinP2:
                possibleOutput.append("wall")
            walls.pop()
    if player == 2:
        Dist2WinXRatioHazardToLose = distanceToWinP2* (int)(distanceToWinP2/distanceToWinP1)
        if len(pathP1) <= chromosome[0]:
            possibleOutput.append("wall")
        if chromosome[2] == 2:
            walls.append(whereToPlaceWall(positionP1,pathP1[1]))
            testPath = bfs(positionP1, goalsP1, grid, walls)
            if len(testPath) > distanceToWinP1:
                possibleOutput.append("wall")
            walls.pop()
    
    if Dist2WinXRatioHazardToLose <= chromosome[1]:
        possibleOutput.append("move")

    if chromosome[2] == 1:
        possibleOutput.append("wall")

    if len(possibleOutput) == 0:
        finalOutput =  "move" #default action
    if len(possibleOutput) >= 1:
        finalOutput = possibleOutput[0]
    
    if finalOutput == "move" and player == 1:
        return input_to_reach_next(positionP1,pathP1[1])
    if finalOutput == "move" and player == 2:
        return input_to_reach_next(positionP2,pathP2[1])
    if finalOutput == "wall" and player == 1:
        return whereToPlaceWall(positionP2,pathP2[1])
    if finalOutput == "wall" and player == 2:
        return whereToPlaceWall(positionP1,pathP1[1])