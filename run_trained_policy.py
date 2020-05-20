from ppo import CategoricalMLP, GaussianMLP
from run_unity_ppo import UnityEnvWrapper
import torch
import numpy as np
# _, get_action = load_policy_and_env('/home/vld/Desktop/hw1/reacher_results/')
# env = PusherEnv(render=True)

env = UnityEnvWrapper()

state_dims = env.state_shape
act_dims = env.action_shape
hidden_sizes = (64,64,64)

model = GaussianMLP(state_dims + hidden_sizes + act_dims)
model.load_state_dict(torch.load("./models/policy.pt"))
model.eval()

actors = env.step()

while(True):
    states = [actors[ID]['obs'] for ID in actors]
    if(len(states) == 0):
        actors = env.step()
        continue
    pis = [model(torch.as_tensor(state,dtype=torch.float32)) for state in states]
    actions = np.array([pi.sample().numpy() for pi in pis])
    actors =  env.step(actions)