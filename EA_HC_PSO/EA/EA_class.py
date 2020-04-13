#!/usr/bin/env python
from EA.Population import Population
import random


class EA:
    def __init__(self, pop_size, indiv_size, mutation_probability, iteration_count = 100):
        """take the size of the starting population and the size of each individual as parameters"""
        self.population = Population(pop_size, indiv_size, mutation_probability)
        self.mutation_probability = mutation_probability
        self.individual_size = indiv_size
        self.population_size = pop_size
        self.iteration_count = iteration_count
        self.top_fitness_list = []
        self.average_fitness_list = []

    def __getitem__(self, item):
        return self.population[item]

    def get_top_fitness_list(self):
        return self.top_fitness_list

    def get_values(self):
        return self.population

    def get_average_fitness(self):
        return self.average_fitness_list

    def set_average_fitness(self):
        fit = 0
        for i in range(self.population_size):
            fit += self.population[i].get_fitness()

        self.average_fitness_list.append(fit / self.population_size)

    def next_generation(self):
        self.population.next_generation()
        self.top_fitness_list.append(self.population.get_current_best().get_fitness())

    def crossover(self):
        """For now, randomly select 2 parents, generate an offspring and keep only the 2 fittest result in the next
        population """
        index1 = random.randint(0, self.population_size - 1)
        index2 = random.randint(0, self.population_size - 1)
        # in case the same index is chosen twice

        while index1 == index2:
            index2 = random.randint(0, self.population_size - 1)
        child = self.population.crossover(index1, index2)
        print(child)

    def found_solution(self):
        for indiv in self.population:
            if indiv.is_solution():
                return True
        return False

    def run_EA(self):
        while self.found_solution() == False and self.iteration_count > 0:
            self.next_generation()
            print("Current best is: ")
            print(self.population.get_current_best())
            print("with the fitness level: ", self.population.get_current_best().get_fitness())
            self.top_fitness_list.append(self.population.get_current_best().get_fitness())
            self.iteration_count -= 1
        if self.found_solution():
            print("Solution found! ")
            print(self.population.get_current_best())
        else:
            print("We've reached the end of iterations")
    def __len__(self):
        return len(self.population.get_all())

def check():
    state = EA(4, 3, 40)
    population = state.get_values()
    print(population)

    state.next_generation()
    population = state.get_values().__str__()

    print("Next generation: ")
    print(population)


def test_run():
    state = EA(100, 4, 40)
    state.run_EA()
