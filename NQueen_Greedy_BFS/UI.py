# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:33:19 2020

@author: User
"""

from ProblemClass import Problem
from ControllerClass import Controller
from time import time

class UI():
    def __init__(self):
        self.__choice = 0
        self.__size = 0

    def getInput(self):
        print("Choose the size of the array")
        self.__size = int(input("-->"))
        
        print("Choose the solving method: \n 1->Greedy\n 2->DFS ")
        self.__choice = int(input("-->"))
        
        if self.__choice == 0:
            return
        elif self.__choice != 1 and self.__choice != 2:
            print("Invalid input") 
            self.getInput()
    
    def run(self):
        self.getInput()
        problem = Problem(self.__size)
        controller = Controller(problem)
        result = controller.startProgram(self.__choice)
        startClock = time()
        print(controller.printState())
        print(result)
        print('execution time = ', time() - startClock, " seconds")
        
def main():
    #initialise stuff:
    ui = UI()
    ui.run()

main()