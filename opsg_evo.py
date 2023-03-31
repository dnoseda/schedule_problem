import random




POPULATION_SIZE = 100
MUTATION_RATE = 0.01
MAX_GENERATIONS = 1000

def printI(individual):
    print("Rota 1 ->",individual[:4])
    print("Rota 2 ->",individual[4:])


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

devs = ['B1', 'D1', 'B2', 'D2', 'C1', 'A2', 'A1', 'C2']
original_devs_arrange = "-".join(devs)


class EightQueensGA:
    def __init__(self):
        self.population = []
        self.fitness_scores = []
        self.best_solution = None

        for i in range(POPULATION_SIZE):
            individual = random.sample(devs, 8)
#            print(individual[0:4], individual[4:8])
            self.population.append(individual)

    def fitness(self, individual):
        if "-".join(individual)== original_devs_arrange:
            return 0

        conflicts = 0
        conflicts = conflicts + levenshtein_distance("-".join(individual), original_devs_arrange)
        rota1, rota2 = individual[:4],individual[4:]

        for i in range(4):

            # TODO: consider if it first time on schedule

            # same dev
            if rota1[i] == rota2[i]: 
                return 0

            # same boss
            if rota1[i][0] == rota2[i][0]: 
                return 0 #conflicts = conflicts + 1
            
            # adjacent boss
            if i+1<4 and (rota1[i][0] == rota1[i+1][0] or rota2[i][0] == rota2[i+1][0]):
                return 0 #conflicts = conflicts + 1


        return 1 / (conflicts + 1)

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
            self.fitness_scores = [self.fitness(individual) for individual in self.population]
            if 1 in self.fitness_scores:
                self.best_solution = self.population[self.fitness_scores.index(1)]
                break

            fitness_scores_copy = self.fitness_scores.copy()
            fitness_scores_copy.sort(reverse=True)
            best_fit_for_now = fitness_scores_copy[0]

            if self.best_solution is None or self.fitness(self.best_solution) < best_fit_for_now:
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
        print("Original:", self.fitness(devs))
        printI(devs)
        if self.best_solution is not None:
            print("Solution found with score.", self.fitness(self.best_solution))
            printI(self.best_solution)
        else:
            print("No solution found.")



ga = EightQueensGA()
ga.evolve()
ga.print_solution()

