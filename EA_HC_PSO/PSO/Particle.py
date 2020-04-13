from copy import deepcopy

from EA.Individual import Individual

class Particle:
    def __init__(self, indiv_size):
        self.indiv_size = indiv_size
        self.individual = Individual(indiv_size)
        self.values = self.individual.values_list()
        self.velocity_table = [0 for i in range(indiv_size*indiv_size)]
        self.position_table = [i for i in range(indiv_size*indiv_size)]
        self.best_position = self.position_table

    def get_velocity_table(self):
        return self.velocity_table

    def set_velocity(self, new_velocity, index):
        self.velocity_table[index] = new_velocity

    def get_position_table(self):
        return self.position_table

    def set_position(self, new_position, index):
        self.position_table[index] = new_position

    def get_best_position_table(self):
        return self.best_position

    def get_fitness(self):
        return self.individual.get_fitness()

    def is_solution(self):
        self.individual = Individual.copy_individual(self.values)
        return self.individual.is_solution()

    def __str__(self):
        out = ""
        vals = deepcopy(self.values)
        for i in range(self.indiv_size):
            row = ""
            for j in range(self.indiv_size):
                row += vals.pop(0).__str__()
            out += row
            out += '\n'

        return out


