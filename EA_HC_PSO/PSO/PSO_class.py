from PSO.PSO_Population import PSO_population


class PSO:
    def __init__(self, indiv_size, pop_size, neighb_size, iterations):
        self.c1 = 1
        self.c2 = 2.5
        self.w = 1
        self.pop_size = pop_size
        self.indiv_size = indiv_size
        self.neighb_size = neighb_size
        self.population = PSO_population(pop_size, indiv_size)
        self.iterations = iterations
        self.current_best = None
        self.highest_fitness = 0



    def run_pso(self):
        neighbourhood_list = self.population.generate_neighbours(self.neighb_size)
        for i in range(self.iterations):
            self.population.iteration(neighbourhood_list, self.c1, self.c2, self.w // (i + 1))
        sorted_list = [(particle, particle.get_fitness()) for particle in self.population]
        sorted_list.sort(key=lambda v: v[1], reverse =True)
        # get the fittest particle
        fittest_particle = sorted_list[0][0]
        fitness_score = sorted_list[0][1]
        self.current_best = fittest_particle
        self.highest_fitness = fitness_score

    def get_current_best(self):
        return self.current_best

    def get_highest_fitness(self):
        return self.highest_fitness


def test_run():
    pso = PSO(3,100,20,10)
    pso.run_pso()
    print(pso.get_current_best())
    print(pso.get_highest_fitness())




