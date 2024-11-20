from classificator import Classificator
import torch
from game_manual_Truco import Game as Game
import random

def main():

    ACTION_DESCRIPTION = {
        -1: "Tirar carta manual",
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
    
    classificatorP1 = Classificator(655, 11, 1024, 512, 1024, 512).to("cpu")
    classificatorP2 = Classificator(655, 11, 1024, 512, 1024, 512).to("cpu")
    classificatorP1.load_state_dict(torch.load("./trainedModels/truco/paramTesting/model3/agent1_iteration_54000000.pt", weights_only=True))
    classificatorP2.load_state_dict(torch.load("./trainedModels/truco/paramTesting/model3/agent2_iteration_54000000.pt", weights_only=True))
    classificatorP1.eval()
    classificatorP2.eval()

    while(True):
        input("Press enter to play new round...")
        controlsP1 = int(input("Input controls P1 (0 no|1 si): "))
        pointsP1 = int(input("Input puntos partida P1: "))
        pointsP2 = int(input("Input puntos partida P2: "))

        game = Game(pointsP1, pointsP2, controlsP1)
        s = game.getState()

        print("-----------------")
        print(f"Round Started ({game.puntosPartidaP1}-{game.puntosPartidaP2})")

        while(not game.gameFinished()):
            #print("+++")
            #print("State: ", s)
            if(game.getIsP1Turn()):
                print("-------------")
                print("Plays P1")
                if(controlsP1):
                    actionIdx = int(input("Choose action: "))
                else:
                    #game.printStateP1()
                    actionLogits = classificatorP1(torch.tensor(s, dtype=torch.float, device="cpu"))
                    actionProbabilities = actionLogits.softmax(dim=0).detach()
            
                    """ print("------")
                    print("Probabilities:")
                    for i in range(11):
                        print(i,ACTION_DESCRIPTION[i], round(actionProbabilities[i].item(),3)) """
                    actionIdx = random.choices(range(11), weights=actionProbabilities, k=1)[0]
                    print("Chosen action:", ACTION_DESCRIPTION[actionIdx])

            else:
                print("-------------")
                print("Plays P2")
                #game.printStateP2()
                if(not controlsP1):
                    actionIdx = int(input("Choose action: "))
                else:
                    #game.printStateP2()
                    actionLogits = classificatorP2(torch.tensor(s, dtype=torch.float, device="cpu"))
                    actionProbabilities = actionLogits.softmax(dim=0).detach()
            
                    """ print("------")
                    print("Probabilities:")
                    for i in range(11):
                        print(i,ACTION_DESCRIPTION[i], round(actionProbabilities[i].item(),3)) """
                    actionIdx = random.choices(range(11), weights=actionProbabilities, k=1)[0]
                    print("Chosen action:", ACTION_DESCRIPTION[actionIdx])
            
            (s1, r1, t1) = game.step(actionIdx)
            input("ENTER TO CONTINUE")
            s = s1[:]
            
        print("-------------")
        print(f"Game Ended ({game.puntosPartidaP1}-{game.puntosPartidaP2})")


if __name__ == '__main__':
    main()
