import random
import torch
from torch import nn

from dqn import DQN
from replayMemory import ReplayMemory
from classificator import Classificator
from reservoirMemory import ReservoirMemory

class Agent:

    def __init__(self, isMano, params):
        self.lastState = None
        self.lastAction = None
        self.lastActionFollowedEpsilonGreedy = False
        self.isWaitingForFeedback = False

        if(not torch.cuda.is_available()):
            print("Cuda not available.")
            raise("Cuda not available.")
        self.device = 'cpu' if torch.cuda.is_available() else 'cpu'

        self.isMano = isMano
        self.hyperparameter_set = params
        #DQN params
        self.DQN_learning_rate_a    = params["dqn_params"]['learning_rate_a']        # learning rate (alpha)
        self.DQN_discount_factor_g  = params["dqn_params"]['discount_factor_g']      # discount rate (gamma)
        self.DQN_updates_between_target_sync  = params["dqn_params"]['updates_between_target_sync']
        self.DQN_steps_between_optimization  = params["dqn_params"]['steps_between_optimization']
        self.DQN_replay_memory_size = params["dqn_params"]['replay_memory_size']     # size of replay memory
        self.DQN_mini_batch_size    = params["dqn_params"]['mini_batch_size']        # size of the training data set sampled from the replay memory
        self.DQN_epsilon_init       = params["dqn_params"]['epsilon_init']           # 1 = 100% random actions
        self.DQN_epsilon_min        = params["dqn_params"]['epsilon_min']            # minimum epsilon value
        self.DQN_anticipatory_parameter = params["dqn_params"]['anticipatory_parameter']            # minimum epsilon value
        self.DQN_input_layer_size = params["dqn_params"]['input_layer_size']
        self.DQN_hidden_layer1_size = params["dqn_params"]['hidden_layer1_size']
        self.DQN_hidden_layer2_size = params["dqn_params"]['hidden_layer2_size']
        self.DQN_hidden_layer3_size = params["dqn_params"]['hidden_layer3_size']
        self.DQN_hidden_layer4_size = params["dqn_params"]['hidden_layer4_size']
        self.DQN_output_layer_size = params["dqn_params"]['output_layer_size']
        self.DQN_enable_double_dqn  = params["dqn_params"]['enable_double_dqn']    # double dqn on/off flag

        #Classification params
        self.MCC_learning_rate_a    = params["classification_params"]['learning_rate_a']
        self.MCC_steps_between_optimization  = params["classification_params"]['steps_between_optimization']
        self.MCC_input_layer_size = params["classification_params"]['input_layer_size']
        self.MCC_hidden_layer1_size = params["classification_params"]['hidden_layer1_size']
        self.MCC_hidden_layer2_size = params["classification_params"]['hidden_layer2_size']
        self.MCC_hidden_layer3_size = params["classification_params"]['hidden_layer3_size']
        self.MCC_hidden_layer4_size = params["classification_params"]['hidden_layer4_size']
        self.MCC_output_layer_size = params["classification_params"]['output_layer_size']
        self.MCC_reservoir_memory_size = params["classification_params"]['reservoir_memory_size']
        self.MCC_mini_batch_size    = params["classification_params"]['mini_batch_size'] 
        self.MCC_min_prob_of_replacing_reservoir = params["classification_params"]['min_prob_of_replacing_reservoir']

        #DQN init        
        self.policy_dqn = DQN(self.DQN_input_layer_size, self.DQN_output_layer_size, self.DQN_hidden_layer1_size, self.DQN_hidden_layer2_size, self.DQN_hidden_layer3_size, self.DQN_hidden_layer4_size).to(self.device)
        self.target_dqn = DQN(self.DQN_input_layer_size, self.DQN_output_layer_size, self.DQN_hidden_layer1_size, self.DQN_hidden_layer2_size, self.DQN_hidden_layer3_size, self.DQN_hidden_layer4_size).to(self.device)
        self.target_dqn.load_state_dict(self.policy_dqn.state_dict())
        
        self.memory_dqn = ReplayMemory(self.DQN_replay_memory_size)
        self.epsilon_dqn = self.DQN_epsilon_init
        self.optimizer_dqn = torch.optim.SGD(self.policy_dqn.parameters(), lr=self.DQN_learning_rate_a)
        self.loss_fn_dqn = nn.MSELoss()

        #MCC init
        self.classificator = Classificator(self.MCC_input_layer_size, self.MCC_output_layer_size, self.MCC_hidden_layer1_size, self.MCC_hidden_layer2_size, self.MCC_hidden_layer3_size, self.MCC_hidden_layer4_size).to(self.device)

        self.memory_mcc = ReservoirMemory(self.MCC_reservoir_memory_size, minProbOfReplacement=self.MCC_min_prob_of_replacing_reservoir)
        self.loss_fn_mcc = nn.CrossEntropyLoss()
        self.optimizer_mcc = torch.optim.SGD(self.classificator.parameters(), lr=self.MCC_learning_rate_a)
        
        self.step_counter = 0
        self.update_counter = 0

    def chooseActionWithEpsilonGreedy(self):
        self.lastActionFollowedEpsilonGreedy = True
        if(random.random() < self.epsilon_dqn):
            chosenIdx = random.choice(range(self.DQN_output_layer_size))
           
            self.lastAction = torch.tensor(chosenIdx, dtype=torch.int64, device=self.device)
        else:
            self.policy_dqn.eval()
            with torch.no_grad():
                chosen = self.policy_dqn(self.lastState.unsqueeze(dim=0)).squeeze()
                if(chosen[0]!=chosen[0]): raise("Network output was NAN")
                chosenIdx = chosen.argmax().item()
                self.lastAction = torch.tensor(chosenIdx, dtype=torch.int64, device=self.device)
    
    def chooseActionWithPolicy(self):
        self.classificator.eval()
        self.lastActionFollowedEpsilonGreedy = False
        with torch.no_grad():
            actionLogits = self.classificator(self.lastState)
            if(actionLogits[0]!=actionLogits[0]): raise("Network output was NAN")
            actionProbabilities = torch.softmax(actionLogits, dim=0)

            chosenIdx = torch.distributions.categorical.Categorical(probs=actionProbabilities).sample().item()
            
            self.lastAction = torch.tensor(chosenIdx, dtype=torch.int64, device=self.device)


    def chooseAction(self, state):
        self.lastState = torch.tensor(state, dtype=torch.float, device=self.device)

        if(random.random() < self.DQN_anticipatory_parameter):
            self.chooseActionWithEpsilonGreedy()
            
        else:
            self.chooseActionWithPolicy()

        self.isWaitingForFeedback = True
        self.step_counter += 1
        self.epsilon_dqn = max(self.DQN_epsilon_init/(self.step_counter**0.5), self.DQN_epsilon_min)

        return self.lastAction.item()
    
    def receiveFeedback(self, newState, reward, terminated):
        if(not self.isMano):
            reward = -reward

        newState = torch.tensor(newState, dtype=torch.float, device=self.device)
        reward = torch.tensor(reward, dtype=torch.float, device=self.device)
        
        if(self.lastActionFollowedEpsilonGreedy):
            #add last state and action to reservoir
            self.memory_mcc.append((self.lastState[:], self.lastAction))

        #Store transition to replay memory
        self.memory_dqn.append((self.lastState[:], self.lastAction, newState[:], reward, terminated))
        self.lastState = None
        self.lastAction = None
        self.isWaitingForFeedback = False

        #optimize dqn
        if (len(self.memory_dqn)>self.DQN_mini_batch_size and self.step_counter%self.DQN_steps_between_optimization==0):
            mini_batch = self.memory_dqn.sample(self.DQN_mini_batch_size)
            self.optimize_dqn(mini_batch)
            self.update_counter += 1

        # optimize mcc
        if (len(self.memory_mcc)>self.MCC_mini_batch_size and self.step_counter%self.MCC_steps_between_optimization==0):
            mini_batch = self.memory_mcc.sample(self.MCC_mini_batch_size)
            self.optimize_mcc(mini_batch)
        
        if (self.update_counter%self.DQN_updates_between_target_sync==0):
            self.target_dqn.load_state_dict(self.policy_dqn.state_dict())
        

    def optimize_dqn(self, mini_batch):
        self.policy_dqn.train()
        self.target_dqn.eval()
        states, actions, new_states, rewards, terminations = zip(*mini_batch)
    
        states = torch.stack(states)

        actions = torch.stack(actions)

        new_states = torch.stack(new_states)

        rewards = torch.stack(rewards)

        terminations = torch.tensor(terminations).float().to(self.device)

        with torch.no_grad():
            if (self.DQN_enable_double_dqn):
                best_actions_from_policy = self.policy_dqn(new_states).argmax(dim=1)

                output = self.target_dqn(new_states).gather(dim=1, index=best_actions_from_policy.unsqueeze(dim=1)).squeeze()

                target_q = rewards + (1-terminations) * self.DQN_discount_factor_g * output
            else:
                # Calculate target Q values (expected returns)
                output = self.target_dqn(new_states).max(dim=1)[0]
                target_q = rewards + (1-terminations) * self.DQN_discount_factor_g * output

        

        # Calcuate Q values from current policy
        current_q = self.policy_dqn(states).gather(dim=1, index=actions.unsqueeze(dim=1)).squeeze()
        # Compute loss
        loss = self.loss_fn_dqn(current_q, target_q)
        if(loss.item()!=loss.item() or loss.item()>100000):
            raise Exception("Loss invalid")
        #print(loss, self.isMano)

        # Optimize the model (backpropagation)
        self.optimizer_dqn.zero_grad()  # Clear gradients
        loss.backward()             # Compute gradients
        self.optimizer_dqn.step()       # Update network parameters i.e. weights and biases

    def optimize_mcc(self, mini_batch):
        self.classificator.train()

        states, actions= zip(*mini_batch)

        states = torch.stack(states)
        actions = torch.stack(actions)
        actions = torch.tensor([[1.0 if idx==a else 0 for idx in range(self.MCC_output_layer_size)] for a in actions], device=self.device)

        actionsLogits = self.classificator(states)

        loss = self.loss_fn_mcc(actionsLogits, actions)
        if(loss.item()!=loss.item() or loss.item()>100):
            raise Exception("Loss invalid")
        #print(loss, self.isMano)

        # Optimize the model (backpropagation)
        self.optimizer_mcc.zero_grad()  # Clear gradients
        loss.backward()             # Compute gradients
        self.optimizer_mcc.step()       # Update network parameters i.e. weights and biases

    def getIsWaitingForFeedback(self):
        return self.isWaitingForFeedback
    
    def showReplayMemory(self):
        self.memory_dqn.show()

    def showReservoirMemory(self):
        self.memory_mcc.show()

    def saveAvgPolicy(self, path):
        torch.save(self.classificator.state_dict(), path)

    def saveGreedyPolicy(self, path):
        torch.save(self.policy_dqn.state_dict(), path)