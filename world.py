import numpy as np
import matplotlib.pyplot

class World(object):
    def __init__(self, n, m, magic_squares, holes, walls):
        self.grid = np.zeros((n,m))
        self.m = m
        self.n = n  
        self.holes = holes
        self.walls = walls

        self.stateSpace = [i for i in range(self.n*self.m)]
        self.stateSpace.pop()
        self.stateSpacePlus = [i for i in range(self.n*self.m)]

        self.actionSpace = {'U':-self.m, 'D':self.m, 'L':-1, 'R':1}
        self.possibleActons = ['U', 'D', 'L', 'R']

        self.add_magic_squares(magic_squares)

        self.agentPosition = 0 

    def add_magic_squares(self, magic_squares):
        self.magic_squares =  magic_squares
        source, destination = 2, 3
        for square in self.magic_squares.keys():
            x = square // self.m
            y  = square % self.n
            self.grid[x][y] = source
            source += 1
            x = magic_squares[square] // self.m
            y = magic_squares[square] % self.n
            self.grid[x][y] = destination
            desitination += 1

    def is_terminal_space(self, state):
        return state in self.stateSpacePlus and state not in self.stateSpace
    
    def get_row_column(self):
        x = self.agentPosition // self.m
        y = self.agentPosition % self.n
        return x,y

    def setState(self, state):
        x,y = self.get_row_column()
        self.grid[x][y] = 0 
        self.agentPosition = state 
        x,y = self.get_row_column()
        self.grid[x][y] = 1

    def offGrid(self, newState, oldState):
        if newState not in self.stateSpacePlus:
            return True

        elif oldState % self.m == 0 and newState % self.m == self.m - 1:
            return True
        elif oldState % self.m == self.m-1 and newState % self.m == 0:
            return True
        else:
            return False

    def step(self, action):
        x,y = self.get_row_column()
        resultingState = self.agentPosition + self.actionSpace[action]
        if resultingState in self.magic_squares:
            resultingState = self.magicSquare[resultingState]
        reward = -1 if not self.is_terminal_space(resultingState) else 0 
        if not self.offGrid(resultingState, self.agentPosition):
            self.setState(resultingState)
            return resultingState, reward, self.is_terminal_space(self.agentPosition), None
        else: 
            return self.agentPosition, reward, self.is_terminal_space(self.agentPosition), None
    def reset(self):
        self.agentPosition = 0
        self.grid = np.zeros((self.n,self.m))
        self.add_magic_squares()
        return self.agentPosition

    def render(self):
        print("-------------------")
        for row in self.grid:
            for col in row:
                if col == 0:
                    print("-")
                if col == 1:
                    print("AG")
                elif col % 2 == 0:
                    print("MI")
                else:
                    print("MO")
        print("-------------------")

            

    

        



        