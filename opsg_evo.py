import random




POPULATION_SIZE = 100
MUTATION_RATE = 0.01
MAX_GENERATIONS = 1000


devs = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]


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
        conflicts = 0

        for i in range(4):

            # same dev
            if individual[i] == individual[i+4]: 
                conflicts = conflicts + 1

            # same boss
            if individual[i][0] == individual[i+4][0]: 
                conflicts = conflicts + 1
            
            # adjacent boss
            if individual[i][0] == individual[i+1][0]: 
                conflicts = conflicts + 1

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

            fitness_scores_copy = self.fitness_scores.copy()
            fitness_scores_copy.sort(reverse=True)
            best_fit_for_now = fitness_scores_copy[0]

            if self.best_solution is None or self.fitness(self.best_solution) < best_fit_for_now:
                best_for_now = self.population[self.fitness_scores.index(best_fit_for_now)]
                self.best_solution = best_for_now
                print("Best_Fit:", best_fit_for_now, "sol:", best_for_now)

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
            print("Solution found with score.", self.fitness(self.best_solution))
            print(self.best_solution[:4])
            print(self.best_solution[4:])
        else:
            print("No solution found.")

ga = EightQueensGA()
ga.evolve()
ga.print_solution()

