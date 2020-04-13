import copy
from random import random, choice

from PSO.Particle import Particle


class PSO_population:
    def __init__(self, pop_size, indiv_size):
        self.pop_size = pop_size
        self.indiv_size = indiv_size
        self.population = []
        self.fitness_list = []

        for i in range(pop_size):
            self.population.append(Particle(indiv_size))

    def __getitem__(self, item):
        return self.population[item]

    def get_population(self):
        return self.population

    def generate_neighbours(self, neighbourhood_size):
        '''Split the population into given-size neighbourhoods'''
        if neighbourhood_size > self.pop_size:
            neighbourhood_size = self.pop_size

        new_neighbours = []
        '''Group the particles in neighbourhoods of given size
        Choose the particles in a '''
        intial_values = copy.deepcopy(self.population)
        while len(intial_values) > 0:
            particle_neighbours = []
            for j in range(neighbourhood_size):
                if len(intial_values) == 0:
                    break
                val = choice(intial_values)
                particle_neighbours.append(val)
                intial_values.remove(val)
            new_neighbours.append(particle_neighbours)
        return new_neighbours

    def get_fitness_list(self):
        return self.fitness_list

    def iteration(self, neighbourhood_list, c1, c2, w):
        '''parse through the particles in the population and compute a new velocity and position'''

        '''compute the fittest neighbour'''
        fittest_neighbour = neighbourhood_list[0][0]
        for i in range(len(neighbourhood_list)):
            fittest_neighbour = neighbourhood_list[i][0]
            for j in range(1, len(neighbourhood_list[i])):
                best_fitness = fittest_neighbour.get_fitness()
                current_fitness = neighbourhood_list[i][j].get_fitness()
                if(current_fitness > best_fitness):
                    fittest_neighbour = neighbourhood_list[i][j]
        self.fitness_list.append(fittest_neighbour.get_fitness())
        '''compute the new velocity'''
        for i in range(self.pop_size):
            for j in range(len(self.population[0].get_velocity_table())):
                velocity = self.population[i].get_velocity_table()[j]
                new_velocity = w * velocity + c1 * random() *((fittest_neighbour.get_position_table()[j]) -self.population[i].get_position_table()[j])
                new_velocity += c2 * random() * (self.population[i].get_best_position_table()[j] - self.population[i].get_position_table()[j])
                self.population[i].set_velocity(new_velocity, j)

        '''update the positions'''
        for i in range(self.pop_size):
            for j in range(len(self.population[0].get_velocity_table())):
                new_position = self.population[i].get_position_table()[j] + self.population[i].get_velocity_table()[j]
                self.population[i].set_position(new_position, j)

        return self.population

