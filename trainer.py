import yaml
from tqdm import tqdm

from agent import Agent as Agent
from game_Truco import Game as Game

def main():
    with open('trainerParams.yml', 'r') as params_file:
        params = yaml.safe_load(params_file)
    
    modelSelected = 5
    params = params[f"model{modelSelected}"] #seleccion de modelo

    print("Started training...")
    agent1 = Agent(True, params["training_params"])
    agent2 = Agent(False, params["training_params"])

    episodes = params["training_params"]["episodes"]
    for iteration in tqdm(range(episodes)):
        #print("------")
        #print("newGame")
        game = Game()
        s = game.getState()
        r = 0
        t = False

        #print(f"puntosPartida: ({game.puntosPartidaP1}-{game.puntosPartidaP2})")

        while(not game.gameFinished()):
            if(game.getIsP1Turn()):
                actionIdx = agent1.chooseAction(s[:])
                #print("agent1 chose",actionIdx)
            else:
                actionIdx = agent2.chooseAction(s[:])
                #print("agent2 chose",actionIdx)

            
            (s1, r1, t1) = game.step(actionIdx)
            s = s1[:]
            r = r1
            t = t1
            
            if((game.getIsP1Turn() or game.gameFinished()) and agent1.getIsWaitingForFeedback()):
                #print("Agent 1 recieved",r)
                agent1.receiveFeedback(s[:], r, t)

            if(((not game.getIsP1Turn()) or game.gameFinished()) and agent2.getIsWaitingForFeedback()):
                #print("Agent 2 recieved",r)
                agent2.receiveFeedback(s[:], r, t)


        if(iteration%1000000==0):
            #save model for testing
            agent1.saveAvgPolicy(f"./trainedModels/truco/paramTesting/model{modelSelected}/agent1_iteration_{iteration}.pt")
            agent1.saveGreedyPolicy(f"./trainedModels/truco/paramTesting/model{modelSelected}/agent1_greedy_iteration_{iteration}.pt")
            agent2.saveAvgPolicy(f"./trainedModels/truco/paramTesting/model{modelSelected}/agent2_iteration_{iteration}.pt")
            agent2.saveGreedyPolicy(f"./trainedModels/truco/paramTesting/model{modelSelected}/agent2_greedy_iteration_{iteration}.pt")

if __name__ == '__main__':
    main()
