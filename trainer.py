import yaml
from tqdm import tqdm

from agent import Agent as Agent
from game_Truco import Game as Game

def main():
    with open('trainerParams.yml', 'r') as params_file:
        params = yaml.safe_load(params_file)

    
    print("Started training...")
    agent1 = Agent(True, params["training_params"])
    agent2 = Agent(False, params["training_params"])

    episodes = params["training_params"]["episodes"]
    for iteration in tqdm(range(episodes)):
        game = Game()
        s = game.getState()
        r = 0
        t = False

        #print("-----------------")
        while(not game.gameFinished()):
            #print("+++")
            #print("State: ", s)
            if(game.getIsP1Turn()):
                actionIdx = agent1.chooseAction(s[:])
            else:
                actionIdx = agent2.chooseAction(s[:])
            
            (s1, r1, t1) = game.step(actionIdx)
            s = s1[:]
            r = r1
            t = t1
            #print("Did:",actionIdx)
            #print("Returned: ", s, r, t)
            #print("Whoose turn:", game.getIsP1Turn())
            if((game.getIsP1Turn() or game.gameFinished()) and agent1.getIsWaitingForFeedback()):
                #print("P1 recieved feedback")
                agent1.receiveFeedback(s[:], r, t)

            if(((not game.getIsP1Turn()) or game.gameFinished()) and agent2.getIsWaitingForFeedback()):
                #print("P2 recieved feedback")
                agent2.receiveFeedback(s[:], r, t)


        if(iteration%1000000==0):
            #save model for testing
            agent1.saveAvgPolicy("./trainedModels/truco/paramTesting/model1/agent1_iteration_{iteration}.pt".format(iteration=iteration))
            agent1.saveGreedyPolicy("./trainedModels/truco/paramTesting/model1/agent1_greedy_iteration_{iteration}.pt".format(iteration=iteration))
            agent2.saveAvgPolicy("./trainedModels/truco/paramTesting/model1/agent2_iteration_{iteration}.pt".format(iteration=iteration))
            agent2.saveGreedyPolicy("./trainedModels/truco/paramTesting/model1/agent2_greedy_iteration_{iteration}.pt".format(iteration=iteration))
    agent1.saveAvgPolicy("./trainedModels/truco/agent1.pt")
    agent1.saveGreedyPolicy("./trainedModels/truco/agent1_greedy.pt")
    agent2.saveAvgPolicy("./trainedModels/truco/agent2.pt")
    agent2.saveGreedyPolicy("./trainedModels/truco/agent2_greedy.pt")

if __name__ == '__main__':
    main()
