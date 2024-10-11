class Game:
    """ 
    Used to simulate a round of Truco.
    Need to be given initial points 
    """
    """ 
    rewardMatrix = [[0, -1, 1],
                    [1, 0, -1],
                    [-1, 1, 0]]
     """
    
    #modified rps
    rewardMatrix = [[0, -2, 1],
                    [2, 0, -1],
                    [-1, 1, 0]]
    
    gameEnded = False
    
    def __init__(self, pointsP1, pointsP2):
        self.actionP1 = None #[piedra, papel, tijera]
        self.actionP2 = None
        self.isP1Turn = True   

    def getState(self):
        if(self.gameEnded): return [0,0]
        if(self.isP1Turn): return [1,0]
        else: return [1,1]

    def getTerminalValue(self):
        if((self.actionP1 is None) or (self.actionP2 is None)):
            return 0
        return self.rewardMatrix[self.actionP1][self.actionP2]


    def step(self, action):
        actionTakenIdx=action

        if(self.isP1Turn):
            self.actionP1 = actionTakenIdx
            self.isP1Turn=False
            return (self.getState(), 0, self.gameEnded)
        else:
            self.actionP2 = actionTakenIdx
            self.gameEnded = True
            return (self.getState(), self.getTerminalValue(), self.gameEnded)


    def gameFinished(self):
        return self.gameEnded
    
    def getIsP1Turn(self):
        return self.isP1Turn

