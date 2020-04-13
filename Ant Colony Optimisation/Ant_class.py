import copy
from itertools import permutations
from random import *
import numpy as np


class Ant:
    def __init__(self, n):
        self.size = n
        self.values = np.zeros(self.size * self.size, dtype=object)
        self.path = []
        self.global_values = []
        self.set_global_values()
        '''The global values will be a list of all possible permutations, in order.
        Each permutation from the list of global values will have an index.
        An ant's path will represent a list of indexes from the gloval_values list, through which the ant has passed,
        How each permutation is ordered is the final answer'''

    def heuristic(self):
        pass

    def get_global_values(self):
        return self.global_values

    def insert_element(self, pos):
        # get the value of the permutation from that position
        value = self.global_values[pos]
        for i in range(len(self.values)):
            # find the first empty position in the list
            if self.values[i] == 0:
                # insert the element on that position
                self.values[i] = value
                # update the path
                self.path.append(pos)
                # remove from the list of global values the permutation that was added to the solution
                # self.global_values.remove(value)
                # the removal part does not happen anymore
                break

    def remove_last_element(self, pos):
        for i in range(len(self.values) - 1, 0, -1):
            if self.values[i] == self.global_values[pos]:
                self.values[i] = 0
        self.path.pop()
    def set_global_values(self):
        all_values = np.zeros((self.size, self.size), dtype=tuple)
        elems = np.arange(1, self.size + 1, 1)
        perm = list(permutations(elems, 2))
        # now set the values for each position in the matrix
        for row in range(self.size):
            for i in range(self.size):
                if row != i:
                    self.global_values.append(perm.pop(0))
                else:
                    self.global_values.append((i + 1, i + 1))

    def copy_ant(self, values, path):
        self.values = values
        self.path = path
        return self

    def valid(self):
        '''Checks if the current values from the path are inserted in a valid formation'''
        values_array = np.zeros((self.size, self.size), dtype=object)
        val_index = 0
        i = 0
        j = 0
        while self.values[val_index] != 0 and val_index < self.size:
            values_array[i][j] = self.values[val_index]
            j += 1
            val_index += 1
            if j == self.size:
                i += 1
                j = 0

        for i in range(self.size):
            left = []
            right = []
            down_left = []
            down_right = []
            for j in range(self.size):
                # look for duplicates in every row and column
                if values_array[i][j] != 0:
                    if values_array[i][j][0] in left:
                        return False
                    left.append(values_array[i][j][0])

                    if values_array[i][j][1] in right:
                        return False
                    right.append(values_array[i][j][1])
                if values_array[j][i] != 0:
                    if values_array[j][i][0] in down_left:
                        return False
                    down_left.append(values_array[j][i][0])

                    if values_array[j][i][1] in down_right:
                        return False
                    down_right.append(values_array[j][i][1])
        return True

    def get_fitness(self):
        return self.size*self.size - len(self.path)
    def get_path(self):
        return self.path
    def next_valid_moves(self, added_position = -1):
        '''returns a list of valid that can be made from the current status'''
        valid_positions = []
        copy_vals = copy.deepcopy(self.values)
        copy_path = copy.deepcopy(self.path)
        new_ant = self.copy_ant(copy_vals, copy_path)
        if added_position != -1:
            new_ant.insert_element(added_position)
        for pos in range(len(self.global_values)):
            if pos not in self.path:
                new_ant.insert_element(pos)
                if new_ant.valid():
                    valid_positions.append(pos)
                new_ant.remove_last_element(pos)
        return valid_positions
    def empirical_distance(self, added_position):
        '''returns the empirical distance resulted from adding the position to the path'''
        return self.size**self.size - len(self.next_valid_moves(added_position))

    def add_next_move(self, q0, trace, alpha, beta):
        '''adds a new element to the values list and a new position to the path, if possible'''
        positions = [0 for i in range(self.size*self.size)]
        next_moves = self.next_valid_moves()
        if len(next_moves) == 0:
            return False
        for i in next_moves:
            positions[i] = self.empirical_distance(i)
        positions = [(positions[i] ** beta) * (trace[self.path[-1]][i] ** alpha) for i in range(len(positions))]
        if random() < q0:
            # if entered this branch, add the best available move to the current path
            positions = [[i, positions[i]] for i in range(len(positions))]
            positions = max(positions, key=lambda v: v[1])
            self.path.append(positions[0])
        else:
            # if entered this branch, add a random possible move
            s = sum(positions)
            if s == 0:
                return choice(next_moves)
            positions = [positions[i] / s for i in range(len(positions))]
            positions = [sum(positions[0:i +1]) for i in range(len(positions))]
            r = random()
            i = 0
            while r > positions[i] and i < len(positions):
                i += 1
            self.path.append(i)
        return True

    def set_starting_position(self):
        '''function that gives the ant a random starting point from the list of global values'''
        start = randint(0, self.size*self.size - 1)
        self.values[0] = self.global_values[start]
        self.path.append(start)

    def __str__(self):
        out = ""
        for j in range(len(self.values)):
            if self.values[j] == 0:
                out += "(0, 0)"
            else:
                out += self.values[j].__str__()
            out += "  "
            if (j + 1) % self.size == 0:
                out += "\n"
        return out
def check_ant():
    ant = Ant(3)
    ant.insert_element(0)
    # print(ant.values)
    # print(ant.next_valid_moves(0))
    print(ant)

# check_ant()
