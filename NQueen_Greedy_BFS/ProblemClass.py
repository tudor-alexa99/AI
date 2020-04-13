# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:09:24 2020

@author: User
"""

import numpy as np
from StateClass import State
from ConfigurationClass import Configuration
class Problem:
    def __init__(self, _n):
        self.values = np.zeros((_n, _n), dtype = int)
        self.n = _n
        self.states = State()
    
    def expand(self, GivenState):
        '''Add the given state into the list of states and return the list '''
        self.states.append(GivenState)
        return self.states
    
    def getValues(self):
        return self.values
    
    def heuristic(self, config):
        #the heuristic function return the number of offprings the current state can generate
        offsprings = len(Configuration(config).nextConfig())
        return offsprings
    
    def Greedy(self):
        #create an empty state and an empty configuration
        #each step, generate the next configuration for the last config added to the state path 
        #once you're done, check if the last configuration generated is a valid result. if it is, return it. Else, return a message
        stateList = State()
        config = Configuration(self.values)
        stateList.add(config)
        for i in range(self.n):
            currentConfig = stateList.getStates()[-1]
            options = currentConfig.nextConfig()
            optionsSorted = [[opt, self.heuristic(opt)] for opt in options]
            optionsSorted.sort(key = lambda v : v[1])
            if len(options) != 0:
                nextC = Configuration(optionsSorted[0][0])
                stateList.add(nextC)
            else:
                self.states = stateList
                return "We've reached a dead end!"
        self.states = stateList
        return "Solution found"

    
    def DFS(self, config):
        self.states.add(config)
        if Configuration(config).totalMoves(config) == True:
            return config
        elif len(Configuration(config).nextConfig()) == 0:
            return None
        options = Configuration(config).nextConfig()
        for attemp in range(len(options)):
            nextConfig = options.pop(0)
            if Configuration(nextConfig).checkAll(nextConfig) == True and Configuration(nextConfig).totalMoves(nextConfig) == self.n:
                break
                return nextConfig
            res = self.DFS(nextConfig)
            try:
                if res != None:
                    return res
            except ValueError:
                return res
    def getStates(self):
        return self.states
    
def testProblem():
    problem = Problem(4)
#    print(problem.DFS(problem.values))
#    print(problem.DFS([[0,1,0,0],[0,0,0,1],[1,0,0,0],[0,0,1,0]]))
    print(problem.heuristic(problem.values))
    
#testProblem()
    
    