from EA.Individual import Individual
from copy import deepcopy


class Hill_Climbing:
    def __init__(self, indiv_size, iteration_count = 100):
        self.indiv_size = indiv_size
        self.current_cell = Individual(indiv_size)
        self.restart_count = 0
        self.iteration_count = iteration_count
    def get_current_cell(self):
        return self.current_cell

    def generate_neighbours(self):
        '''For the current value, generate a list of neighbours by swapping all the combination of 2 values possible
        Sort the list of neighbours by their fitness level
        Choose the fittest one out of the bunch as the current_cell
        Continue until a solution is found'''
        neighbours = []
        # we'll use the values_list() and empty_individual() functions, in order to avoid 4 for loops
        starting_values = self.current_cell.values_list()

        for i in range(len(starting_values) - 1):
            for j in range(i + 1, len(starting_values)):
                swapped_values = deepcopy(starting_values)
                swapped_values[i], swapped_values[j] = swapped_values[j], swapped_values[i]

                neighbour = Individual(self.indiv_size)
                neighbour.empty_individual()
                neighbour.list_to_individual(swapped_values)

                neighbours.append(neighbour)
        return neighbours

    def get_best_neighbour(self, neighbours_list):
        sorted_list = [[neighbour, neighbour.get_fitness()] for neighbour in neighbours_list]
        sorted_list.sort(key=lambda v: v[1], reverse=True)
        return sorted_list[0][0]

    def solution_found(self):
        return self.current_cell.is_solution()

    def run_hc(self):
        while not self.solution_found() and self.iteration_count > 0:
            neighbours = self.generate_neighbours()
            best_neighbour = self.get_best_neighbour(neighbours)
            if self.current_cell.get_fitness() >= best_neighbour.get_fitness() and not best_neighbour.is_solution():
                self.random_restart()
                print(" >>> Random restart <<<")
            else:
                self.current_cell = best_neighbour
                print(self.current_cell)
            self.iteration_count -= 1
        if self.solution_found():
            print("solution found!")
            print(self.current_cell)
            print("After a number of ", self.restart_count, " restarts")
        else:
            print("Iteration count reached 0")

    def random_restart(self):
        '''If called, it means we've reached a local optimum that is not a solution, so a new cell is generated'''
        self.current_cell = Individual(self.indiv_size)
        self.restart_count += 1


def test_run():
    hc = Hill_Climbing(3)
    hc.run_hc()
