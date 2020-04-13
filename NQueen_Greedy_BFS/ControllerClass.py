# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:02:08 2020

@author: User
"""

class Controller:
    def __init__(self, problem):
        self.__problem = problem
    
    def startProgram(self, method):
        if method == 1:
            return str(self.__problem.Greedy())
        elif method == 2:
            return str(self.__problem.DFS(self.__problem.getValues()))
    
    def printState(self):
        return "\nThe list of states:\n" + str(self.__problem.getStates())
    