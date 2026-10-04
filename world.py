import numpy as np
import matplotlib.pyplot as plt

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

        self.addMagicSquares(magic_squares)

        self.agentPosition = 0 

    def addMagicSquares(self, magic_squares):
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
            destination += 1

    def isTerminalSpace(self, state):
        return state in self.stateSpacePlus and state not in self.stateSpace
    
    def getRowColumn(self):
        x = self.agentPosition // self.m
        y = self.agentPosition % self.n
        return x,y

    def setState(self, state):
        x,y = self.getRowColumn()
        self.grid[x][y] = 0 
        self.agentPosition = state 
        x,y = self.getRowColumn()
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
        x,y = self.getRowColumn()
        resultingState = self.agentPosition + self.actionSpace[action]
        if resultingState in self.magic_squares:
            resultingState = self.magic_squares[resultingState]
        reward = -1 if not self.isTerminalSpace(resultingState) else 0 
        if not self.offGrid(resultingState, self.agentPosition):
            self.setState(resultingState)
            return resultingState, reward, self.isTerminalSpace(self.agentPosition), None
        else: 
            return self.agentPosition, reward, self.isTerminalSpace(self.agentPosition), None
    def reset(self):
        self.agentPosition = 0
        self.grid = np.zeros((self.n,self.m))
        self.addMagicSquares(self.magic_squares)
        return self.agentPosition

    def render(self):
        print("-------------------")
        for row in self.grid:
            for col in row:
                if col == 0:
                    print("-", end="  ")
                elif col == 1:
                    print("AG", end=" ")
                elif col % 2 == 0:
                    print("MI", end=" ")
                else:
                    print("MO", end=" ")
            print()
        print("-------------------")

    def actionSpaceSample(self):
        return np.random.choice(self.possibleActons)

def maxAction(Q, state, actions):
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return actions[action]


if __name__ == '__main__':
    magic_squares = {18:58, 40:20, 47:62}
    env = World(9,9, magic_squares, None, None)

    alpha = 0.1
    gamma = 1
    epsilon = 1.0

    Q = {}
    for state in env.stateSpacePlus:
        for action in env.possibleActons:
            Q[state, action] = 0

    games = 50000
    rewards= np.zeros(games)
    env.render()
    for i in range(games):
        if i == 0:
            print("Game Start")
        done = False
        epRewards= 0 
        observation = env.reset()

        while not done:
            rand = np.random.random()
            action = maxAction(Q, observation, env.possibleActons) if  rand < 1 - epsilon \
                else env.actionSpaceSample()
            
            observation_, reward, done, info = env.step(action)
            epRewards += reward
            action_ = maxAction(Q, observation_, env.possibleActons)
            Q[observation, action] = Q[observation, action] + alpha* (reward + \
                gamma *  Q[observation_, action_]  - Q [observation, action])
            observation = observation_
        
        epsilon = max(0, epsilon - 2 / games)
        rewards[i] = epRewards
    plt.plot(rewards)
    plt.show()
        
                
            





    

        



        