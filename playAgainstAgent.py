from classificator import Classificator
from dqn import DQN
import torch
from game_Truco import Game as Game

import numpy as np
import random

def main():
    
    classificator = Classificator(655, 11, 512, 1024, 512, 1024).to("cpu")
    classificator.load_state_dict(torch.load("./trainedModels/truco/agent1.pt", weights_only=True))
    classificator.eval()
    greedy = DQN(655, 11, 512, 1024, 512, 1024).to("cpu")
    greedy.load_state_dict(torch.load("./trainedModels/truco/agent1_greedy.pt", weights_only=True))
    greedy.eval()

    game = Game()
    s = game.getState()
    r = 0
    t = False

    print("-----------------")
    print("Game Started")
    print("-----------------")
    print("Hand P1:", game.handP1)
    print("Hand P2:", game.handP2)
    print("-----------------")

    while(not game.gameFinished()):
        #print("+++")
        #print("State: ", s)
        if(not game.getIsP1Turn()):
            print("-------------")
            print("-------------")
            print("-------------")
            print("-------------")
            print("P2 Turn")
            game.printStateP2()

            actionIdx = int(input("Choose action: "))
        else:
            print("-------------")
            print("-------------")
            print("-------------")
            print("-------------")
            print("P1 Turn")
            game.printStateP1()

            actionLogits = classificator(torch.tensor(s, dtype=torch.float, device="cpu"))
            actionProbabilities = actionLogits.softmax(dim=0).detach()

            print("Action probabilities:",actionProbabilities)
            q = greedy(torch.tensor(s, dtype=torch.float, device="cpu"))
            print("Q-values:",q)

            actionIdx = random.choices(range(11), weights=actionProbabilities, k=1)[0]
            print("Chosen action:", actionIdx)
        
        (s1, r1, t1) = game.step(actionIdx)
        s = s1[:]
         
        
        #print("Whoose turn:", game.getIsP1Turn())
        if(game.gameFinished()):
            print("-------------")
            print("Game Ended")


if __name__ == '__main__':
    main()
