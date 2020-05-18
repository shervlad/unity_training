import torch
import torch.nn as nn
import numpy as np
from torch.optim import Adam
from torch.distributions.normal import Normal
import csv
class GaussianMLP(torch.nn.Module):
    def __init__(self, dimensions, activation = nn.ReLU, output_activation=nn.Tanh):
        super().__init__()

        layers = []

        for j in range(len(dimensions)-1):
            act = activation if j < len(dimensions)-2 else output_activation
            layers += [nn.Linear(dimensions[j], dimensions[j+1]), act()]

        self.log_std = nn.Parameter(torch.as_tensor(-0.5*np.ones(dimensions[-1],dtype=np.float32)))
        self.perceptron =  nn.Sequential(*layers)

    def forward(self, state):
        pi = self.perceptron(state)
        st_dev = torch.exp(self.log_std)
        return Normal(pi,st_dev)

class CategoricalMLP(torch.nn.Module):
    def __init__(self,dimensions,activation = nn.ReLU, output_activation=nn.Identity):
        super().__init__()
        layers = []

        for j in range(len(dimensions)-1):
            act = activation if j < len(dimensions)-2 else output_activation
            layers += [nn.Linear(dimensions[j], dimensions[j+1]), act()]

        self.perceptron =  nn.Sequential(*layers)

    def forward(self, state):
        return torch.squeeze(self.perceptron(state),-1)

def discount(arr, gamma, last_val = 0):
    T = len(arr)
    discounted = [last_val]*(T+1)

    for i in range(T):
        discounted[-i-2] = arr[-i-1] + gamma*discounted[-i-1]

    return discounted[:-1]

def compute_advatages(states,rewards,vals,gamma,last_val):
    T = len(states)
    deltas = [0]*T
    for i in range(T):
        nextval = last_val
        if(i != T-1):
            nextval = vals[i+1]
        deltas[i] = rewards[i] + gamma*nextval - vals[i]

    a = discount(deltas,gamma,last_val)
    return a

class Buffer:
    def __init__(self):
        self.actorsBuffers = {}

    def add(self, ID, state, action, reward, val, logp):
        if ID not in self.actorsBuffers:
            self.actorsBuffers[ID] = {'states':[],'actions':[],'rewards':[],'vals':[],'logprobs':[]} 
        self.actorsBuffers[ID]['states'].append(state)
        self.actorsBuffers[ID]['actions'].append(action)
        self.actorsBuffers[ID]['rewards'].append(reward)
        self.actorsBuffers[ID]['vals'].append(val)
        self.actorsBuffers[ID]['logprobs'].append(logp)

    def get(self,actor):
        res = [self.actorsBuffers[actor]['states'], \
               self.actorsBuffers[actor]['actions'],\
               self.actorsBuffers[actor]['rewards'],\
               self.actorsBuffers[actor]['vals'],   \
               self.actorsBuffers[actor]['logprobs']]

        self.actorsBuffers[actor]['states']   = []
        self.actorsBuffers[actor]['actions']  = []
        self.actorsBuffers[actor]['rewards']  = []
        self.actorsBuffers[actor]['vals']     = []
        self.actorsBuffers[actor]['logprobs'] = []
        return res

    def addActor(self,actor):
        if actor not in self.actorsBuffers:
            self.actorsBuffers[actor] = {'states':[],'actions':[],'rewards':[],'vals':[],'logprobs':[]} 

    def addState(self,actor,state):
        self.addActor(actor);
        self.actorsBuffers[actor]['states'].append(state)

    def addAction(self,actor,action):
        self.addActor(actor);
        self.actorsBuffers[actor]['actions'].append(action)

    def addReward(self,actor,reward):
        self.addActor(actor);
        self.actorsBuffers[actor]['rewards'].append(reward)

    def addVal(self,actor,val):
        self.addActor(actor);
        self.actorsBuffers[actor]['vals'].append(val)

    def addLogProb(self,actor,logp):
        self.addActor(actor);
        self.actorsBuffers[actor]['logprobs'].append(logp)

def ppo(env_fn, num_epochs=10000, steps_per_epoch=400, gamma=0.98, lam = 0.95, epsilon = 0.2, 
        pi_step=0.0001, v_step = 0.001, sgd_iterations=20, plot_fn = None, path=None):

    env = env_fn()

    buffer = Buffer()

    state_dims = env.state_shape
    act_dims   = env.action_shape

    hidden_sizes = (64,64)

    pi_network = GaussianMLP(state_dims + hidden_sizes + act_dims)
    v_network  = CategoricalMLP(state_dims + hidden_sizes + (1,))

    pi_optimizer = Adam(pi_network.parameters(), lr = pi_step)
    v_optimizer = Adam(v_network.parameters(), lr = v_step)

    def update(trajectory):
        #update
        states,actions,rewards,vals,log_probs = trajectory

        states     = torch.as_tensor(states, dtype=torch.float32)
        actions    = torch.as_tensor(actions, dtype=torch.float32)
        rewards    = torch.as_tensor(rewards, dtype=torch.float32)
        vals       = torch.as_tensor(vals, dtype=torch.float32)
        log_probs  = torch.as_tensor(log_probs, dtype=torch.float32)

        #compute advantages
        last_val = vals[-1]
        adv        = torch.as_tensor(compute_advatages(states,rewards,vals, gamma*lam, last_val), dtype=torch.float32)
        returns    = torch.as_tensor(discount(rewards,gamma,last_val), dtype=torch.float32)


        pi_losses = []
        v_losses  = []
        for i in range(sgd_iterations):

            #calculate loss pi
            pi_optimizer.zero_grad()
            pi = pi_network(states)
            new_log_probs = pi.log_prob(actions).sum(axis=-1)
            ratio = torch.exp(new_log_probs - log_probs)
            l_cpi = torch.clamp(ratio,1-epsilon,1+epsilon)*adv
            loss_pi = -1*(torch.min(ratio*adv, l_cpi)).mean()
            pi_losses.append(loss_pi.item())
            loss_pi.backward()
            pi_optimizer.step()
            
        for i in range(sgd_iterations):
            v_optimizer.zero_grad()
            loss_v = ((v_network(states) - returns)**2).mean()
            v_losses.append(loss_v.item())
            loss_v.backward()
            v_optimizer.step()

        mean_loss_pi = np.array(pi_losses).mean()
        mean_loss_v  = np.array(v_losses).mean()

    actors = env.step()
    for idx, ID in enumerate(actors):
        if(not actors[ID]['done']):
            buffer.addState(ID,actors[ID]['obs'])

    e = 0
    while e<num_epochs:
        print("Epoch %s"%e)


        states = [actors[a]['obs'] for a in actors]

        if(len(states) == 0):
            actors = env.step()
            continue

        pis = [pi_network(torch.as_tensor(state, dtype=torch.float32)) for state in states]
        actions = np.array([pi.sample().numpy() for pi in pis])
        print("ACTIONS")
        print(np.matrix(actions))
        logp =  np.array([pis[i].log_prob(torch.FloatTensor(actions[i])).sum(axis=-1) for i in range(len(pis))])
        v = v_network(torch.as_tensor(states, dtype=torch.float32))

        print("value network: ",v)
        for idx, ID in enumerate(actors):
            buffer.addAction(ID,actions[idx])
            buffer.addLogProb(ID,logp[idx])
            buffer.addVal(ID,v[idx])

        new_actors = env.step(actions)

        for idx, ID in enumerate(new_actors):
            if(new_actors[ID]['done']):
                buffer.addReward(ID,new_actors[ID]['reward'])
                trajectory = buffer.get(ID)
                update(trajectory)
                e+=1
                buffer.addState(ID,new_actors[ID]['obs'])
            else:
                buffer.addReward(ID,new_actors[ID]['reward'])
                buffer.addState(ID,new_actors[ID]['obs'])


        actors = new_actors

        # if(e%10 == 0):
        #     plot_fn(env = env, epoch = e, pi = pi_network, v_net=v_network)
        #     save_metrics(e,rewards,vals,mean_loss_pi,mean_loss_v,path)

        if(e%50 == 0 and path is not None):
            print("saving...")
            save(pi_network, v_network, path)





def save(pi_network, v_network,path):
    torch.save(pi_network.state_dict(),path+"policy.pt")
    torch.save(v_network.state_dict(),path+"value_fn.pt")

def save_metrics(epoch,rewards,vals,mean_loss_pi,mean_loss_v,path):
    cum_r = np.sum(rewards.detach().numpy())
    min_r = rewards.min().item()
    max_r = rewards.max().item()
    mean_r = rewards.mean().item()
    min_v = vals.min().item()
    max_v = vals.max().item()
    mean_v = vals.mean().item()
    with open(path+'metrics.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([epoch,cum_r,min_r,mean_r,max_r,min_v,mean_v,max_v,mean_loss_pi,mean_loss_v])