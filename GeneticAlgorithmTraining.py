import sys

#Retrieving the chromosome population

def ChromosomePopulationGeneration(population_number):
    chromosomePopulation = []
    for i in range(population_number):
        chromosome = [random.randint(chromosome_composition[gene_name][0],chromosome_composition[gene_name][1]) for gene_name in chromosome_composition]
        chromosomePopulation.append(chromosome)
    return chromosomePopulation

print("Path of the input file of the desired chromosome population : ")
inputPath = sys.stdin.readline()
inputPath = inputPath.rstrip("\n")

f = open(inputPath,"r")
chromosomePopulation = f.read()
f.close()
chromosomePopulation = eval(chromosomePopulation) #List of chromosome population

#Now we want to confront each model against 