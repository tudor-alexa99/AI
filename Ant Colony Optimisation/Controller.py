from Ant_class import Ant


class Controller:
    def __init__(self,input_file):
        self.input_file = input_file
        self.ant_size = 0
        self.trace = None
        self.alpha = None
        self.beta = 0
        self.q0 = 0
        self.rho = 0
        self.iteration_count = 0
        self.ant_number = 0
        self.load_params()
        self.best_path = []
        self.best_ant = None

    def get_best_ant(self):
        return self.best_ant
    def get_iter_count(self):
        return self.iteration_count
    def get_ant_size(self):
        return self.ant_size
    def new_colony(self):
        colony = []
        for i in range(self.ant_number):
            ant = Ant(self.ant_size)
            # set the starting position for each ant
            ant.set_starting_position()
            colony.append(ant)

        for i in range(self.ant_size*self.ant_size):
            for ant in colony:
                ant.add_next_move(self.q0, self.trace, self.alpha, self.beta)

        pheromone_trace = [1.0 / colony[i].get_fitness() for i in range(len(colony))]
        for i in range(self.ant_number):
            for j in range(len(colony[i].path) - 1):
                a = colony[i].path[j]
                b = colony[i].path[j+1]
                self.trace[a][b] += pheromone_trace[i]
        # return the main ant's path
        sorted_ants = [[colony[i].get_fitness(), i] for i in range(len(colony)) ]
        queen_ant = max(sorted_ants)
        # return colony[queen_ant[1]].path
        self.best_ant = colony[queen_ant[1]]
        self.best_path = self.best_ant.path
    def load_params(self):
        with open(self.input_file, 'r') as file:
            line = file.readline().strip()
            self.iteration_count = int(line.replace("Iteration count:", ""))

            line = file.readline().strip()
            self.ant_number = int(line.replace("Ants number:", ""))

            line = file.readline().strip()
            self.ant_size = int(line.replace("Ant size:", ""))

            line = file.readline().strip()
            self.alpha = float(line.replace("alpha:", ""))

            line = file.readline().strip()
            self.beta = float(line.replace("beta:", ""))

            line = file.readline().strip()
            self.rho = float(line.replace("rho:", ""))

            line = file.readline().strip()
            self.q0 = float(line.replace("q0:", ""))

            self.trace = [[1 for i in range(self.ant_size*self.ant_size)] for j in range(self.ant_size*self.ant_size)]