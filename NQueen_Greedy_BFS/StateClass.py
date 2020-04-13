# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:14:21 2020

@author: User
"""


class State:
    '''hold a path of configuration'''

    def __init__(self):
        self.__values = []
        
    def getStates(self):
        return self.__values
    
    def __str__(self):
        out = ""
        for i in self.__values:
            out += i.__str__()
            out += '\n\n'
        return out
    def pop(self):
        return self.__values.pop()
    def add(self, config):
        self.__values.append(config)
        
        