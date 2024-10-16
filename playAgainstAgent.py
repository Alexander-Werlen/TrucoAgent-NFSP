from classificator import Classificator
from dqn import DQN
import torch
from game_Truco import Game as Game
import time
import numpy as np
import random

def main():

    ACTION_DESCRIPTION = {
        0: "Tirar C1",
        1: "Tirar C2",
        2: "Tirar C3",
        3: "Aceptar Envido",
        4: "Rechazar Envido",
        5: "Envido",
        6: "Real envido",
        7: "Falta envido",
        8: "Aceptar Truco",
        9: "Rechazar Truco",
        10: "Bet truco"
    }
    
    classificator = Classificator(655, 11, 512, 1024, 512, 1024).to("cpu")
    #classificator.load_state_dict(torch.load("./trainedModels/truco/paramTesting/model1/agent2_iteration_5000000.pt", weights_only=True))
    classificator.load_state_dict(torch.load("./trainedModels/truco/paramTesting/model1/agent2_iteration_27000000.pt", weights_only=True))
    classificator.eval()
    greedy = DQN(655, 11, 512, 1024, 512, 1024).to("cpu")
    greedy.load_state_dict(torch.load("./trainedModels/truco/paramTesting/model1/agent2_greedy_iteration_27000000.pt", weights_only=True))
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
        if(game.getIsP1Turn()):
            print("-------------")
            print("-------------")
            print("-------------")
            print("-------------")
            print("P1 Turn")
            #game.printStateP1()

            actionIdx = int(input("Choose action: "))
        else:
            print("-------------")
            print("-------------")
            print("-------------")
            print("-------------")
            print("P2 Turn")
            game.printStateP2()

            actionLogits = classificator(torch.tensor(s, dtype=torch.float, device="cpu"))
            actionProbabilities = actionLogits.softmax(dim=0).detach()
    
            print("------")
            print("Probabilities:")
            for i in range(11):
                print(i,ACTION_DESCRIPTION[i], round(actionProbabilities[i].item(),3))

            q = greedy(torch.tensor(s, dtype=torch.float, device="cpu"))
            print("------")
            print("Q values:")
            for i in range(11):
                print(i,ACTION_DESCRIPTION[i], round(q[i].item(),3))

            actionIdx = random.choices(range(11), weights=actionProbabilities, k=1)[0]
            print("Chosen action:", ACTION_DESCRIPTION[actionIdx])
        
        (s1, r1, t1) = game.step(actionIdx)
        s = s1[:]
         
        
        #print("Whoose turn:", game.getIsP1Turn())
        if(game.gameFinished()):
            print("-------------")
            print("Game Ended")


if __name__ == '__main__':
    main()
