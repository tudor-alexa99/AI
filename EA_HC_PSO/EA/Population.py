from EA.Individual import Individual
import numpy as np
import random


class Population:
    def __init__(self, population_size, individual_size, mutation_probability):
        '''create a list of individuals with a given size'''
        self.values = []
        self.size = population_size
        self.individual_size = individual_size
        self.mutation_probability = mutation_probability
        self.initialise_population()
        self.best_fitness = 0
        self.current_best = None # we'll keep the Individual with the highest fitness score here

    def __getitem__(self, item):
        return self.values[item]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __str__(self):
        out = ""
        for v in self.values:
            out += v.__str__()
            out += "\n"
        return out

    def get_current_best(self):
        return self.current_best

    def get_all(self):
        return self.values


    def next_generation(self):
        ''' Pair each consecutive parents with each other, both ways around (as in P1 X P2 and P2 X P1)
        It will result in 2*__n children
        Sort the resulted children by their fitness level
        Only keep the first __n fittest offsprings '''
        options = []
        for i in range(len(self.values) - 1):
            child1 = self.crossover(i, i + 1)
            child2 = self.crossover(i + 1, i)
            self.values.append(child1)
            self.values.append(child2)


        # sort the offsprings by fitness
        options_sorted = [[opt, opt.get_fitness()] for opt in self.values]
        options_sorted.sort(key=lambda v: v[1], reverse=True)
        self.current_best = options_sorted[0][0]
        self.best_fitness = self.current_best.get_fitness()
        # overwrite the current population:
        for i in range(self.size):
            self.values[i].__eq__(options_sorted[i][0])

        #remove the rest of the elements
        while len(self.values) != self.size:
            self.values.pop()

    def crossover(self, parent1, parent2):
        '''
        parent1 and parent2 are indexes!!
        Version #1 :
        take 2 parents and cross them
        the result will be a child with 50-50 genes from each parent
        the genes will be selected by positions:
        > even position: take the gene from parent 1
        > odd position: take the gene from parent 2
        Implementation moved to the 'ideas' file
        '''

        '''
        Version #2:
        Use the Order Crossover algorithm
        Design a function that returns the values of each individual as linear lists (for ease of use)
        '''
        child = Individual(self.individual_size, self.mutation_probability)
        child.empty_individual()
        child = child.values_list()
        parent1 = self.values[parent1].values_list()
        parent2 = self.values[parent2].values_list()
        start = random.randint(0, len(parent1) - 2) # used -2 in order to avoid getting the very last position
        stop = random.randint(start + 1, len(parent1) - 1)
        for i in range(start, stop):
            child[i] = parent1[i]
        # parse through the second parent and wrap the values in the child
        # child_step = the index of the position from the child we're currently in (is to be set back to 0 when we've reached the end)
        # parent_step = the index from the parent where we choose the value from
        parent_step = stop

        remaining_values = []
        for parent_step in range(stop, len(parent2)):
            if parent2[parent_step] not in child:
                remaining_values.append(parent2[parent_step])

        for parent_step in range(0, stop):
            if parent2[parent_step] not in child:
                remaining_values.append(parent2[parent_step])
        for child_step in range (stop, len(child)):
            child[child_step] = remaining_values.pop(0)

        for child_step in range(0, start):
            child[child_step] = remaining_values.pop(0)

        new_child = Individual(self.individual_size, self.mutation_probability)
        child_step = 0

        for i in range(self.individual_size):
            for j in range(self.individual_size):
                new_child.set_value(i, j, child[child_step])
                child_step += 1
        # mutate the child:
        new_child.mutate()
        return new_child

    def initialise_population(self):
        for i in range(self.size):
            indiv = Individual(self.individual_size, self.mutation_probability)
            self.values.append(indiv)
