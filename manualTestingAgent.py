from classificator import Classificator
from dqn import DQN
import torch

def main():
    classificator = Classificator(9, 4, 64, 0, 0, 0).to("cpu")
    classificator.load_state_dict(torch.load("./trainedModels/kuhn/agent1.pt", weights_only=True))
    classificator.eval()
    state = torch.tensor([0, 1, 0, 0, 0, 0, 0, 1, 0], dtype=torch.float, device="cpu")
    actionLogits = classificator(state)
    print("Action logits:",actionLogits)
    actionProbabilities = actionLogits.softmax(dim=0)
    print("Action probabilities:",actionProbabilities)

    policy_dqn = DQN(9, 4, 64, 0, 0, 0).to("cpu")
    policy_dqn.load_state_dict(torch.load("./trainedModels/kuhn/agent1_greedy.pt", weights_only=True))
    policy_dqn.eval()
    q = policy_dqn(state)
    print("Q-values:",q)

if __name__ == '__main__':
    main()