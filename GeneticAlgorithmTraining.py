import sys
from fitnessFunction import calculate_fitness
from PathfindingPlayer import *
import Q20
import random


fitness_scores = []
#Now we want to train this population
chromosome_composition = {
    "EffDistOPP2WinBeforeUsingWall": [1,4],
    "Dist2WinXRatioHazardToLose": [1,100],
    "PutAWallIfIncreasesOpponentPath": [0,2]
}

def gradientToWin(player, game):
    grid = [[0 for i in range(5)] for j in range(5)]
    walls = transformBoardToWallsTuple(game.board)
    if player == 1:
        goals = [(0,i) for i in range(5)]
        actualPosition = game.player_positions.get('P1')
    elif player == 2:
        goals = [(4,i) for i in range(5)]
        actualPosition = game.player_positions.get('P2')
    gradient_to_win = 1 - (bfs(actualPosition, goals, grid, walls)/25)
    return gradient_to_win
    
def ChromosomePopulationGeneration(population_size):
    chromosomePopulation = []
    for i in range(population_size):
        chromosome = [random.randint(chromosome_composition[gene_name][0],chromosome_composition[gene_name][1]) for gene_name in chromosome_composition]
        chromosomePopulation.append(chromosome)
    return chromosomePopulation

def evaluate_chromosome(chromosome1, chromosome2):
    
    # Suppose we have a function to play the game using the chromosome
    game = Q20.Quoridor(board_size=5,player1_chromosome=chromosome1, player2_chromosome=chromosome2)

    if game.game_over:
        P1_walls_placed = 4 - game.walls.get("P1")
        P2_walls_placed = 4 - game.walls.get("P2")

        if game.player_positions["P1"][0] == 0:
            P2_gradient_to_win= gradientToWin(2, game)
            fitness1 = calculate_fitness(True, P1_walls_placed, P2_walls_placed, None, P2_gradient_to_win)
            fitness2 = calculate_fitness(False, P1_walls_placed, P2_walls_placed, P2_gradient_to_win, None)
        elif game.player_positions["P2"][0] == 4:
            P1_gradient_to_win = gradientToWin(1, game)
            fitness2 = calculate_fitness(True, P2_walls_placed, P1_walls_placed, None, P1_gradient_to_win)
            fitness1 = calculate_fitness(False, P1_walls_placed, P2_walls_placed, P1_gradient_to_win, None)
        return {fitness1,fitness2}

def evaluate_population(population1,population2):
    fitness_scores = [[] for i in range(2)]
    for i in range(len(population1)):
        fitness = evaluate_chromosome(population1[i],population2[i])
        fitness_scores[0].append(fitness[0])
        fitness_scores[1].append(fitness[1])
    return fitness_scores

def rank_selection(fitness_scores, population):
    sorted_population1 = [chromosome for _, chromosome in sorted(zip(fitness_scores[0], population), reverse=True)]
    top_two = sorted_population1[:2]

    return top_two

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(chromosome, mutation_rate=0.1):
    if random.random() < mutation_rate:
        mutation_point = random.randint(0, len(chromosome) - 1)
        if mutation_point == 0:
            chromosome[mutation_point] = random.randint(1, 4)
        elif mutation_point == 1:
            chromosome[mutation_point] = random.randint(1, 100)
        else:
            chromosome[mutation_point] = random.randint(0, 2)

    return chromosome

def create_new_population(selected_population, population_size):
    new_population = selected_population.copy()
    
    # Ajouter 4 nouveaux chromosomes aléatoires
    new_population.extend(ChromosomePopulationGeneration(4))
    
    # Ajouter 4 nouveaux chromosomes à partir du croisement et de la mutation
    while len(new_population) < population_size:
        parent1, parent2 = random.sample(selected_population, 2)
        child1, child2 = crossover(parent1, parent2)
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))
    
    return new_population[:population_size]

def training(generations, population_size):
    chromosomePopulation1 = ChromosomePopulationGeneration(population_size)
    chromosomePopulation2 = ChromosomePopulationGeneration(population_size)
    print(chromosomePopulation1, chromosomePopulation2)
    for generation in range(generations):
        fitness_scores = evaluate_population(chromosomePopulation1, chromosomePopulation2)

        selected_population1 = rank_selection(fitness_scores, chromosomePopulation1)
        chromosomePopulation1 = create_new_population(selected_population1, population_size)

        selected_population2 = rank_selection(fitness_scores, chromosomePopulation2)
        chromosomePopulation2 = create_new_population(selected_population2, population_size)


        
        print(f"Generation {generation}: Best Fitness = {max(fitness_scores)}")

# Initialisation
print("zhgzjeg")
training(generations=10, population_size=10)