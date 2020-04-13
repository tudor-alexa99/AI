import numpy as np
import random
from itertools import permutations


class Individual:
    def __init__(self, __n, mutation_probability=0):
        self.size = __n
        self.values = np.zeros((__n, __n), dtype=tuple)
        self.init_values()
        self.optimal_fitness = (__n * (__n + 1)) / 2
        self.mutation_probability = mutation_probability
        self.fitness = self.compute_fitness()

    def empty_individual(self):
        self.values = np.zeros((self.size, self.size), dtype=tuple)

    def list_to_individual(self, values_list):
        for i in range(self.size):
            for j in range(self.size):
                self.set_value(i, j, values_list.pop(0))

    def set_value(self, i, j, val):
        self.values[i][j] = val

    def get_values(self):
        return self.values

    def copy_individual(self, other_values):
        self.values = other_values
        return self

    def init_values(self):
        '''function that generates a permutation_probability list of the n values and gives random values to the individual
        note: you'll need to add separately the values (x,x), (y,y)... to the list
        '''
        elems = np.arange(1, self.size + 1, 1)
        perm = list(permutations(elems, 2))
        for i in range(1, self.size + 1):
            perm.append((i, i))
        # now set the values for each position in the matrix
        for row in self.values:
            for i in range(len(row)):
                row[i] = random.choice(perm)
                perm.remove(row[i])

    def values_list(self):
        elems = []
        for row in self.values:
            for i in row:
                elems.append(i)
        return elems

    def swap_values(self, i1, j1, i2, j2):
        '''swap the values from indexes [i1][j2] and [i2][j2]'''
        '''used for the MUTATION method'''
        self.values[i1][j1], self.values[i2][j2] = self.values[i2][j2], self.values[i1][j1]

    def mutate(self):
        """Check if a mutation should be performed
        If yes, randomly swap 2 genes"""
        mutation = random.randint(0, 101)
        if mutation >= self.mutation_probability:
            i1 = random.randint(0, self.size - 1)
            j1 = random.randint(0, self.size - 1)
            i2 = random.randint(0, self.size - 1)
            j2 = random.randint(0, self.size - 1)
            while i1 == i2 and j1 == j2:
                i2 = random.randint(0, self.size - 1)
                j2 = random.randint(0, self.size - 1)
            self.swap_values(i1, j1, i2, j2)
        self.compute_fitness()

    def __str__(self):
        out = ""
        for i in range(self.size):
            out += "["
            for j in range(self.size):
                out += self.values[i][j].__str__()
            out += "]\n"
        return out

    def compute_fitness(self):
        """ go through the pairs from each line/column and compute the sum
        If the sum == optimal_fitness, increase the fitness lever of the current individual """
        fitness = 0
        for tup in range(0, 2):
            for i in range(self.size):
                line_sum = 0
                for j in range(self.size):
                    line_sum += self.values[i][j][tup]
                if line_sum == self.optimal_fitness:
                    fitness += 1
            for i in range(self.size):
                col_sum = 0
                for j in range(self.size):
                    col_sum += self.values[j][i][tup]
                if col_sum == self.optimal_fitness:
                    fitness += 1

        self.fitness = fitness

    def get_fitness(self):
        self.compute_fitness()
        return self.fitness

    def is_solution(self):
        return self.fitness == self.optimal_fitness * 2

    def __eq__(self, other):
        self.values = other.get_values()
        self.fitness = other.get_fitness()


def test_fitness():
    i = Individual(3, 4)
    print(i.values)
    print(i.get_fitness())
