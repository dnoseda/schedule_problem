import random

POPULATION_SIZE = 100
MUTATION_RATE = 0.01
MAX_GENERATIONS = 1000

class EightQueensGA:
    def __init__(self):
        self.population = []
        self.fitness_scores = []
        self.best_solution = None

        for i in range(POPULATION_SIZE):
            individual = random.sample(range(8), 8)
            self.population.append(individual)

    def fitness(self, individual):
        conflicts = 0
        for i in range(len(individual)):
            for j in range(i + 1, len(individual)):
                if individual[i] == individual[j] or \
                   individual[i] - i == individual[j] - j or \
                   individual[i] + i == individual[j] + j:
                    conflicts += 1
        return 1 / (conflicts + 1)

    def select_parents(self):
        parent1 = random.choices(self.population, weights=self.fitness_scores)[0]
        parent2 = random.choices(self.population, weights=self.fitness_scores)[0]
        return parent1, parent2

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, 6)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
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
        if self.best_solution is not None:
            for i in range(8):
                line = ""
                for j in range(8):
                    if self.best_solution[i] == j:
                        line += "Q "
                    else:
                        line += ". "
                print(line)
        else:
            print("No solution found.")

ga = EightQueensGA()
ga.evolve()
ga.print_solution()
