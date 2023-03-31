import random
import time
import sys
from multiprocessing import Pool
import csv


start = time.time()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printT(msg):
    print((time.time()-start), "-->",msg)

POPULATION_SIZE = 1000
MUTATION_RATE = 0.1
MAX_GENERATIONS = 10000

#devs = ['B1', 'D1x', 'B2', 'D2', 'C1', 'A2x', 'A1', 'C2']
devs = ['G5_','H2_','A6_','H6_','B4_','H4x','D2_','D4x','C1x','E3x','E6_','C5_','B2_','E4_','G4_','G2x','F4_','A4_','E1_','C2_','F1_','C6_','H1_','H5_','D5_','C4_','H3x','F3_','F2_','A1_','B1_','E5_','G3_','D3_','A2_','B3_','D1_','D6_','E2_','G1_','B6_','F6_','G6_','B5x','F5_','A3x','C3_','A5_']
original_devs_arrange = "-".join(devs)
half_point = int(len(devs)/2)


def printL(l):
    for i in l:
        if i[0] == 'A':
            print(bcolors.OKBLUE+"_"+i+bcolors.ENDC+", ", end="")
        elif i[0] == 'B':
            print(bcolors.OKGREEN+"_"+i+bcolors.ENDC+", ", end="")
        elif i[0] == 'C':
            print(bcolors.WARNING+"_"+i+bcolors.ENDC+", ", end="")
        elif i[0] == 'D':
            print(bcolors.FAIL+"_"+i+bcolors.ENDC+", ", end="")
        elif i[0] == 'E':
            print(bcolors.BOLD+"_"+i+bcolors.ENDC+", ", end="")
        elif i[0] == 'F':
            print(bcolors.UNDERLINE+"_"+i+bcolors.ENDC+", ", end="")
        elif i[0] == 'G':
            print("+"+i+", ", end="")
        elif i[0] == 'H':
            print("$"+i+", ", end="")
        else:
            print(i+", ", end="")

    print("")

def printI(individual):
    print("Rota 1 -> ",end="")
    printL(individual[:half_point])

    print("Rota 2 -> ",end="")
    printL(individual[half_point:])


def levenshtein_distance(s, t):
    """
    Calculate the Levenshtein distance between two strings s and t using dynamic programming.
    """
    # Initialize a matrix of zeros with dimensions (len(s) + 1) x (len(t) + 1)
    dist = [[0 for j in range(len(t) + 1)] for i in range(len(s) + 1)]

    # Fill in the first row and column of the matrix
    for i in range(1, len(s) + 1):
        dist[i][0] = i
    for j in range(1, len(t) + 1):
        dist[0][j] = j

    # Fill in the rest of the matrix
    for j in range(1, len(t) + 1):
        for i in range(1, len(s) + 1):
            if s[i-1] == t[j-1]:
                cost = 0
            else:
                cost = 1
            dist[i][j] = min(dist[i-1][j] + 1,    # deletion
                             dist[i][j-1] + 1,    # insertion
                             dist[i-1][j-1] + cost) # substitution

    # Return the final Levenshtein distance
    return dist[-1][-1]


def fitness(individual, is_original=False):
    if not is_original and "-".join(individual)== original_devs_arrange:
        return 0.0000001

    conflicts = 0
    conflicts = conflicts + levenshtein_distance("-".join(individual), original_devs_arrange)
    rota1, rota2 = individual[:half_point],individual[half_point:]

    for i in range(half_point):

        # consider if it first time on schedule
        if rota1[i][-1:] == "x" and rota2[i][-1:] == "x":
            conflicts = conflicts + 1000

        # same dev
        if rota1[i] == rota2[i]: 
            conflicts = conflicts + 1000

        # same boss
        if rota1[i][0] == rota2[i][0]: 
            conflicts = conflicts + 1000
        
        # adjacent boss
        if i+1<half_point and (rota1[i][0] == rota1[i+1][0] or rota2[i][0] == rota2[i+1][0]):
            conflicts = conflicts + 1000

    return 1 / (conflicts + 1)



class EightQueensGA:
    def __init__(self):
        self.population = []
        self.fitness_scores = []
        self.best_solution = None
        self.csv_writer = None

        for i in range(POPULATION_SIZE):
            individual = random.sample(devs, len(devs))
            self.population.append(individual)
    def set_csv_writer(self, csv_writer):
        self.csv_writer = csv_writer

    def select_parents(self):
        parent1 = random.choices(self.population, weights=self.fitness_scores)[0]
        parent2 = random.choices(self.population, weights=self.fitness_scores)[0]
        return parent1, parent2

    def crossover(self, parent1, parent2):
        child1 = [None] * len(parent1)
        child2 = [None] * len(parent2)
        i = random.randint(0, len(parent1) - 1)

        # Copy first i elements from parent1 into child1 and from parent2 into child2
        for j in range(i):
            child1[j] = parent1[j]
            child2[j] = parent2[j]

        # Add remaining unique elements from parent2 into child1 and from parent1 into child2
        for element in parent2:
            if element not in child1:
                for j in range(i, len(child1)):
                    if child1[j] is None:
                        child1[j] = element
                        break
            if element not in child2:
                for j in range(i, len(child2)):
                    if child2[j] is None:
                        child2[j] = element
                        break

        for element in parent1:
            if element not in child2:
                for j in range(i, len(child2)):
                    if child2[j] is None:
                        child2[j] = element
                        break
            if element not in child1:
                for j in range(i, len(child1)):
                    if child1[j] is None:
                        child1[j] = element
                        break

        # Remove duplicate elements from child1
        for j in range(i, len(child1)):
            while child1[j] in child1[:j] + child1[j+1:]:
                duplicate_index = child1.index(child1[j], j+1)
                available_elements = set(parent1 + parent2) - set(child1)
                child1[duplicate_index] = random.choice(list(available_elements))

        # Remove duplicate elements from child2
        for j in range(i, len(child2)):
            while child2[j] in child2[:j] + child2[j+1:]:
                duplicate_index = child2.index(child2[j], j+1)
                available_elements = set(parent1 + parent2) - set(child2)
                child2[duplicate_index] = random.choice(list(available_elements))

        return child1, child2

    def mutate(self, individual):
        if random.random() < MUTATION_RATE:
            pos1, pos2 = random.sample(range(8), 2)
            individual[pos1], individual[pos2] = individual[pos2], individual[pos1]

    def evolve(self):
        for i in range(MAX_GENERATIONS):
            printT("start gen "+str(i))

            #self.fitness_scores = [fitness(individual) for individual in self.population]

            with Pool() as pool:
                self.fitness_scores = pool.map(fitness, self.population)

            if 1 in self.fitness_scores:
                self.best_solution = self.population[self.fitness_scores.index(1)]
                break

            self.csv_writer.writerow(self.fitness_scores)

            fitness_scores_copy = self.fitness_scores.copy()
            fitness_scores_copy.sort(reverse=True)
            best_fit_for_now = fitness_scores_copy[0]

            if self.best_solution is None or fitness(self.best_solution) < best_fit_for_now:
                best_for_now = self.population[self.fitness_scores.index(best_fit_for_now)]
                self.best_solution = best_for_now
                print("Best_Fit:", best_fit_for_now)

            new_population = []

            for j in range(int(POPULATION_SIZE / 2)):
                parent1, parent2 = self.select_parents()
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1)
                self.mutate(child2)
                new_population.append(child1)
                new_population.append(child2)

            self.population = new_population

    def print_solution(self):
        print("Original:", fitness(devs, is_original=True))
        printI(devs)
        if self.best_solution is not None:
            print("Solution found with score.", fitness(self.best_solution))
            printI(self.best_solution)
        else:
            print("No solution found.")



if __name__ == '__main__':
    csv_file = open('output_'+str(random.sample(range(88888), 1)[0])+'.csv', 'w')
    writer = csv.writer(csv_file)
    ga = EightQueensGA()
    ga.set_csv_writer(writer)
    try:
        ga.evolve()
        ga.print_solution()
        csv_file.close()
    except KeyboardInterrupt:
        ga.print_solution()
        csv_file.close()
        sys.exit(0)


