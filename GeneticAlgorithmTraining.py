import sys
from fitnessFunction import calculate_fitness
from PathfindingPlayer import *
import Q20Training
import random


fitness_scores = []
#Now we want to train this population
chromosome_composition = {
    "EffDistOPP2WinBeforeUsingWall": [1,25],
    "Dist2WinXRatioHazardToLose": [1,100],
    "PutAWallIfIncreasesOpponentPath": [0,2], #0 Never; 1 Mandatory; 2 Only if path not increase for us
    "PointsBehindToTriggerBlockingOpponent": [0,50],
    "MovingOrWall": [0,1] #0 Moving; 1 Wall
}

def gradientToWin(player, game_state):
    grid = [[0 for i in range(5)] for j in range(5)]
    walls = transformBoardToWallsTuple(game_state["g_board"])
    if player == 1:
        goals = [(0,i) for i in range(5)]
        actualPosition = game_state["g_p1_position"]
    elif player == 2:
        goals = [(4,i) for i in range(5)]
        actualPosition = game_state["g_p2_position"]
    gradient_to_win = 1 - (len(bfs(actualPosition, goals, grid, walls))/25)
    return gradient_to_win
    
def ChromosomePopulationGeneration(population_size):
    chromosomePopulation = []
    for i in range(population_size):
        chromosome = [random.randint(chromosome_composition[gene_name][0],chromosome_composition[gene_name][1]) for gene_name in chromosome_composition]
        chromosomePopulation.append(chromosome)
    return chromosomePopulation

def evaluate_chromosome(chromosome1, chromosome2):
    # Suppose we have a function to play the game using the chromosome
    game_state = Q20Training.Quoridor.run_game(chromosome1, chromosome2)
    
    P1_walls_placed = 4 - game_state["g_walls_p1"]
    P2_walls_placed = 4 - game_state["g_walls_p2"]

    if game_state["g_player_positions_p1_0"] == 0:
        P2_gradient_to_win= gradientToWin(2, game_state)
        fitness1 = calculate_fitness(True, P1_walls_placed, P2_walls_placed, None, P2_gradient_to_win)
        fitness2 = calculate_fitness(False, P1_walls_placed, P2_walls_placed, P2_gradient_to_win, None)
    elif game_state["g_player_positions_p2_0"] == 4:
        P1_gradient_to_win = gradientToWin(1, game_state)
        fitness2 = calculate_fitness(True, P2_walls_placed, P1_walls_placed, None, P1_gradient_to_win)
        fitness1 = calculate_fitness(False, P1_walls_placed, P2_walls_placed, P1_gradient_to_win, None)
    return [fitness1,fitness2]

def evaluate_population(population1,population2):
    fitness_scores = [[] for i in range(2)]
    for i in range(len(population1)):
        fitness = evaluate_chromosome(population1[i],population2[i])
        # print(fitness)
        fitness_scores[0].append(fitness[0])
        fitness_scores[1].append(fitness[1])
    return fitness_scores

def rank_selection(fitness_scores, population, p_type):
    if p_type == 1:
        sorted_population1 = [chromosome for _, chromosome in sorted(zip(fitness_scores[0], population), reverse=True)]
    elif p_type == 2:
        sorted_population1 = [chromosome for _, chromosome in sorted(zip(fitness_scores[1], population), reverse=True)]

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
        elif mutation_point == 2:
            chromosome[mutation_point] = random.randint(0, 2)
        elif mutation_point == 3:
            chromosome[mutation_point] = random.randint(0, 50)
        elif mutation_point == 4:
            chromosome[mutation_point] = random.randint(0, 1)

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
    for generation in range(generations):
        print("new population 1 P1 ",chromosomePopulation1, "new population 1 P2 ", chromosomePopulation2, "gen ", generation)
        fitness_scores = evaluate_population(chromosomePopulation1, chromosomePopulation2)

        selected_population1 = rank_selection(fitness_scores, chromosomePopulation1, p_type=1)
        chromosomePopulation1 = create_new_population(selected_population1, population_size)

        selected_population2 = rank_selection(fitness_scores, chromosomePopulation2, p_type=2)
        chromosomePopulation2 = create_new_population(selected_population2, population_size)


        print(fitness_scores)
        # print(f"Generation {generation}: Best Fitness = {fitness_scores}")

# Initialisation
training(generations=10, population_size=10)