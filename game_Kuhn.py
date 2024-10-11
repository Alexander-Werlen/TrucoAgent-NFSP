import random

class Game:
    
    gameEnded = False
    
    def __init__(self, pointsP1, pointsP2):
        self.isP1Turn = True
        
        #state [{hasA,hasB,hasC},{P1trewA, P1trewB, P1trewC},{P1madeBet, P2madeBet},{hasToRespondBet}]
        self.stateP1 = [0,0,0,0,0,0,0,0,0]
        self.stateP2 = [0,0,0,0,0,0,0,0,0]
        self.finalState = [1,1,1,1,1,1,1,1,1]

        deck = [0,1,2]
        self.cardP1 = random.choice(deck)
        deck.remove(self.cardP1)
        self.cardP2 = random.choice(deck)

        self.stateP1[self.cardP1] = 1
        self.stateP2[self.cardP2] = 1

        self.P1HasToRespond = False
        self.P2HasToRespond = False
        self.betP1 = 1
        self.betP2 = 1

        #print("----------------------------")
        #print("Game started (",self.cardP1,",",self.cardP2,")")
        self.actions  =["throwCard", "makeBet", "acceptBet", "rejectBet"]


    def getState(self):
        if(self.gameEnded): return self.finalState[:]
        if(self.isP1Turn): return self.stateP1[:]
        else: return self.stateP2[:]

    def invalidActionFeedback(self):
        self.gameEnded = True
        if(self.isP1Turn):
            return (self.finalState[:], -1*(self.betP1), self.gameEnded)
        else:
            return (self.finalState[:], 1*(self.betP2), self.gameEnded)

    def step(self, action):
        #action
        #[throwCard, makeBet, acceptBet, rejectBet]
        actionTakenIdx=action
        
        if(self.isP1Turn):
            #print("P1 did",self.actions[actionTakenIdx])

            if(actionTakenIdx==0):
                #Check if invalid
                if(self.P1HasToRespond): return self.invalidActionFeedback()
                ###
                self.isP1Turn = False
                #self.stateP1[3+self.cardP1] = 1
                #self.stateP2[3+self.cardP1] = 1
                
                return (self.getState(), 0, self.gameEnded)
            if(actionTakenIdx==1):
                #Check if invalid
                if(self.P1HasToRespond): return self.invalidActionFeedback()
                if(self.betP1>1): return self.invalidActionFeedback()
                ###
                self.isP1Turn = False
                self.P2HasToRespond = True
                self.betP1 = 2
                self.stateP1[6] = 1
                self.stateP2[6] = 1
                self.stateP2[8] = 1
                return (self.getState(), 0, self.gameEnded)
            if(actionTakenIdx==2):
                #Check if invalid
                if(not self.P1HasToRespond): return self.invalidActionFeedback()
                ###
                self.isP1Turn = False
                self.P1HasToRespond = False
                self.stateP1[8] = 0
                self.betP1 = 2
                return (self.getState(), 0, self.gameEnded)
            if(actionTakenIdx==3):
                #Check if invalid
                if(not self.P1HasToRespond): return self.invalidActionFeedback()
                ###
                self.gameEnded = True
                return (self.finalState, -1*(self.betP1), self.gameEnded)
        elif(not self.isP1Turn):
            #print("P2 did",self.actions[actionTakenIdx])

            if(actionTakenIdx==0):
                #Check if invalid
                if(self.P2HasToRespond): return self.invalidActionFeedback()
                ###

                self.gameEnded=True
                if(self.cardP1>self.cardP2):
                    return (self.finalState, (self.betP2), self.gameEnded)
                else:
                    return (self.finalState, -1*(self.betP1), self.gameEnded)
            if(actionTakenIdx==1):
                #Check if invalid
                if(self.P2HasToRespond): return self.invalidActionFeedback()
                if(self.betP2>1): return self.invalidActionFeedback()
                ###
                self.isP1Turn = True
                self.P1HasToRespond = True
                self.betP2 = 2
                self.stateP1[7] = 1
                self.stateP2[7] = 1
                self.stateP1[8] = 1

                return (self.getState(), 0, self.gameEnded)
            if(actionTakenIdx==2):
                #Check if invalid
                if(not self.P2HasToRespond): return self.invalidActionFeedback()
                ###
                self.isP1Turn = True
                self.P2HasToRespond = False
                self.stateP2[8] = 0
                self.betP2 = 2

                return (self.getState(), 0, self.gameEnded)
            if(actionTakenIdx==3):
                #Check if invalid
                if(not self.P2HasToRespond): return self.invalidActionFeedback()
                ###
                self.gameEnded = True

                return (self.finalState, (self.betP2), self.gameEnded)
    
    def gameFinished(self):
        return self.gameEnded
    
    def getIsP1Turn(self):
        return self.isP1Turn

