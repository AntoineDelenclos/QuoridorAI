import random
import sys

OUTPUT_PATH = "ChromosomePopulation"

chromosome_composition = {
    "EffDistOPP2WinBeforeUsingWall": [1,4],
    "Dist2WinXRatioHazardToLose": [1,100]
}

print(chromosome_composition.values)

def ChromosomePopulationGeneration(population_number):
    chromosomePopulation = []
    for i in range(population_number):
        chromosome = [random.randint(chromosome_composition[gene_name][0],chromosome_composition[gene_name][1]) for gene_name in chromosome_composition]
        chromosomePopulation.append(chromosome)
    return chromosomePopulation

print("Which Player will have this population ?")
player = sys.stdin.readline()
player = player.rstrip("\n")
player = int(player)
print("How much chromosome in your population ?")
populationNumber = sys.stdin.readline()
populationNumber = populationNumber.rstrip("\n")
populationNumber = int(populationNumber)
f = open(str(OUTPUT_PATH+"{}".format(player)+".txt"),"w")
chromosomePopulation = ChromosomePopulationGeneration(population_number=populationNumber)
f.write(str(chromosomePopulation))
f.close()
