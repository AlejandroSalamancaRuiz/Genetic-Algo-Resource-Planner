import numpy as np
import matplotlib.pyplot as plt
import os

# Genetic Algorithm (GA) class definition
class Genetic_Algo():
    def __init__(self, w1, w2, skill_table, months_per_task, cost_per_person, skills_per_task, p_size, p_crossover, p_mutation, p_replacement, max_generations):
        """
        Initialize GA with provided parameters:
        w1, w2: weights for fitness function
        skill_table: matrix representing skills of individuals
        months_per_task: array representing months required for each task
        cost_per_person: array representing cost per person
        skills_per_task: matrix representing required skills per task
        p_size: population size
        p_crossover: crossover probability
        p_mutation: mutation probability
        p_replacement: replacement probability
        max_generations: maximum number of generations
        """
        self.months_per_task = months_per_task
        self.skill_table = skill_table
        self.population_size = p_size
        self.prob_crossover = p_crossover
        self.prob_mutation = p_mutation
        self.max_generations = max_generations
        self.individuals = np.zeros((p_size, skill_table.shape[0], months_per_task.shape[0]))
        self.cost_per_person = cost_per_person
        self.skills_per_task = skills_per_task
        self.w1 = w1
        self.w2 = w2
        self.perc_replacement = p_replacement

    def calculate_costs(self):
        """
        Calculate time, cost, and skill match for each individual in the population.
        """
        time_list, cost_list, skills_match_list = [], [], []

        for i in range(self.individuals.shape[0]):
            time, cost, skills_match = 0, 0, 0

            for k in range(self.individuals.shape[2]):
                total_time_per_task, total_cost_per_task, skills_in_team = 0, 0, []

                for j in range(self.individuals.shape[1]):
                    if self.individuals[i, j, k] != 0:
                        total_time_per_task += self.individuals[i, j, k]
                        total_cost_per_task += self.cost_per_person[j]

                        for l in range(len(self.skill_table[j, :])):
                            if self.skill_table[j, l] == 1 and l not in skills_in_team:
                                skills_in_team.append(l)

                total_time_per_task = self.months_per_task[k] / total_time_per_task
                total_cost_per_task = total_cost_per_task * total_time_per_task

                match = len(skills_in_team) / len(self.skills_per_task[k, :])

                time += total_time_per_task
                cost += total_cost_per_task
                skills_match += match

            skills_match /= self.individuals.shape[2]

            time_list.append(time)
            cost_list.append(cost)
            skills_match_list.append(skills_match)

        max_time = np.sum(self.months_per_task)
        max_cost = np.sum(self.months_per_task * np.max(self.cost_per_person))

        for i in range(len(time_list)):
            time_list[i] /= max_time
            cost_list[i] /= max_cost

        return time_list, cost_list, skills_match_list

    def fitness(self):
        """
        Calculate the fitness of each individual based on time, cost, and skill match.
        """
        fitness_list = []
        time_list, cost_list, validity_list = self.calculate_costs()

        for i in range(len(time_list)):
            fitness_list.append(validity_list[i] * ((self.w1 / cost_list[i]) + (self.w2 / time_list[i])))

        return fitness_list

    def init_population(self):
        """
        Initialize the population with random assignments.
        """

        for i in range(self.population_size):
            for j in range(self.skill_table.shape[0]):
                for k in range(self.months_per_task.shape[0]):
                    self.individuals[i, j, k] = 0.5

    def normalized_and_accumulated_fitness(self):
        """
        Calculate normalized and accumulated fitness for selection.
        """
        fitness_ = self.fitness()
        accumulated_fitness = np.cumsum(fitness_)
        normalized_fitness = fitness_ / accumulated_fitness[-1]

        return fitness_, normalized_fitness, accumulated_fitness

    def roulette_wheel(self):
        """
        Select individuals for crossover using roulette wheel selection.
        """
        selected_individuals = np.zeros((2, self.individuals.shape[1], self.individuals.shape[2]))
        fitness_, _, accumulated_fitness = self.normalized_and_accumulated_fitness()

        for i in range(2):
            eta = np.random.rand() * accumulated_fitness[-1]
            j = 0
            while eta > accumulated_fitness[j]:
                j += 1
            selected_individuals[i, :, :] = self.individuals[j, :, :]

        return selected_individuals

    def crossover(self):
        """
        Perform crossover between individuals to create the next generation.
        """
        next_gen = np.zeros((self.individuals.shape))
        counter = 0
        replacement_quantity = int(self.population_size * self.perc_replacement)

        while counter < self.population_size:
            selected_individuals = self.roulette_wheel()

            i1 = selected_individuals[0, :, :]
            i2 = selected_individuals[1, :, :]

            if counter > replacement_quantity:
                next_gen[counter, :, :] = i1
                next_gen[counter + 1, :, :] = i2
            else:
                p = np.random.rand()
                if p < self.prob_crossover:
                    i = np.random.randint(1, self.individuals.shape[1] - 1)
                    j = np.random.randint(1, self.individuals.shape[2] - 1)

                    new_i1 = np.zeros_like(i1)
                    new_i2 = np.zeros_like(i2)

                    new_i1[0:i, 0:j] = i1[0:i, 0:j]
                    new_i1[i:, j:] = i1[i:, j:]
                    new_i1[0:i, j:] = i2[0:i, j:]
                    new_i1[i:, 0:j] = i2[i:, 0:j]

                    new_i2[0:i, 0:j] = i2[0:i, 0:j]
                    new_i2[i:, j:] = i2[i:, j:]
                    new_i2[0:i, j:] = i1[0:i, j:]
                    new_i2[i:, 0:j] = i1[i:, 0:j]

                    next_gen[counter, :, :] = new_i1
                    next_gen[counter + 1, :, :] = new_i2

            counter += 2

        return next_gen

    def mutation(self, individuals):
        """
        Perform mutation on the population.
        """
        possible_assign = [0, 0.25, 0.5, 0.75, 1]

        for i in range(individuals.shape[0]):
            for j in range(individuals.shape[1]):
                for k in range(individuals.shape[2]):
                    if np.random.rand() < self.prob_mutation:
                        individuals[i, j, k] = possible_assign[np.random.randint(5)]

        return individuals

    def check_constraints(self, individuals):
        """
        Ensure that at least one person is assigned to each task.
        """
        for i in range(individuals.shape[0]):
            for j in range(individuals.shape[2]):
                if np.sum(individuals[i, :, j]) == 0:
                    individuals[i, np.random.randint(individuals.shape[1]), j] = 0.25

        return individuals

    def run_algorithm(self):

        mins, maxs, means = [], [], []
        best_chromosomes = []

        self.init_population()
        self.individuals = self.check_constraints(self.individuals)

        for generation in range(self.max_generations):
            next_gen = self.crossover()
            next_gen = self.mutation(next_gen)
            next_gen = self.check_constraints(next_gen)
            self.individuals = next_gen

            fitness_ = self.fitness()
            best_chromosomes.append(self.individuals[np.argmax(fitness_), :, :])

            maxs.append(np.max(fitness_))
            means.append(np.mean(fitness_))
            mins.append(np.min(fitness_))

        return mins, maxs, means, best_chromosomes

# Function to plot GA results
def plot_ga(mins, maxs, means, output_folder):
    """
    Plot fitness values over generations and save the plot in the output folder.
    """
    plt.figure(figsize=(23,6))
    x = np.arange(len(mins))

    plt.title('Fitness per Generation')
    plt.plot(x, mins, label='Min Fitness')
    plt.plot(x, maxs, label='Max Fitness')
    plt.plot(x, means, label='Mean Fitness')

    plt.legend()
    plt.savefig(os.path.join(output_folder, 'ga_fitness_plot.png'))
    plt.close()


