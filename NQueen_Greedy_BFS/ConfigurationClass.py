# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 15:22:30 2020

@author: User
"""
import copy
class Configuration:
    '''Aici tinem efectiv elementele din matrice, i.e. ce regine sunt asezate si unde'''
    '''Ai functie de nextConfig, in care doar adaugi o regina pe o pozitie _valabila_ '''
    '''Ai nevouie de functiile de validare'''
    
    def __init__(self, values):
        self.__n = len(values) #matrice patratica 
        self.__values = values[:]
        #ai grija ca lucrezi cu matrici, s-ar putea sa nu mearga toate smecheriile de pe liste
    
    def getSize(self):
        return self.__size
    def getValues(self):
        return self.__values[:]
    
    def nextConfig(self):
        #functie care genereaza o noua posibilitate de a aseza o regina pe tabla, in functie de ce avem pana acum
        #apelezi functiile de validare 
        nextC = []
        aux = copy.deepcopy(self.__values)
        
        #iterates through all the possible configurations, and adds the valid ones to the nextConfig table
        for i in range(self.__n):
            for j in range(self.__n):
                if aux[i][j] == 0:
                    aux[i][j] = 1
                    if self.checkAll(aux) == True:
                        nextC.append(aux)
                aux = copy.deepcopy(self.__values)
        return nextC
    
    def checkRow(self, A):
        for i in range (self.__n):
            #for each row, check if there is a value of 1 in it
            found1 = False
            for j in range (self.__n):
                if A[i][j] == 1:
                    if found1 == True:
                        return False
                    else:
                        found1 = True
        return True
    
    def checkColumn(self, A):
        for i in range(self.__n):
            found1 = False
            for j in range(self.__n):
                if A[j][i] == 1:
                    if found1 == True:
                        return False
                    else:
                        found1 = True
        return True
    
    def checkLeftToRight(self, A):
        #optimized version:
        #you only need to parse through a the first n-1 elems in a line and the first n-1 elems in a column to check this sum
        j = 0
        while j < self.__n - 1:
            for i in range (self.__n - 1):
                _i = i+1
                _j = j + 1 
                _sum = A[i][j]
                while(_i < self.__n and _j < self.__n):
                    _sum += A[_i][_j]
                    if _sum > 1:
                        return False
                    _i += 1
                    _j += 1
            j += 1
        return True
    def checkRightToLeft(self, A):
        j =1
        while j < self.__n:
            for i in range(1, self.__n):
                _sum = A[i][j]
                _j = j - 1
                _i = i + 1
                while(_j >= 0 and _i < self.__n):
                    _sum += A[_i][_j]
                    if _sum > 1:
                        return False
                    _i += 1
                    _j -= 1
            j += 1 
        return True
    def checkAll(self, A):
        return self.checkColumn(A) and self.checkRow(A) and self.checkRightToLeft(A) and self.checkLeftToRight(A)
    
    def __str__(self):
        return self.__values.__str__()
    def totalMoves(self, A):
        total = 0
        for i in range(len( self.__values)):
            for j in range(len(self.__values[i])):
                total += self.__values[i][j]
        return total == self.__n
    
def testChecks():
    vals = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]
    config = Configuration(vals)
    print(config.nextConfig())
    
#testChecks()