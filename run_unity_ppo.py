from mlagents_envs.environment import UnityEnvironment, DecisionSteps
import numpy as np
from ppo import ppo


class UnityEnvWrapper:
    def __init__(self):
        self.env = UnityEnvironment(file_name=None, seed=1, worker_id=0, side_channels=[])
        self.env.reset()
        self.behavior_names = [b for b in self.env.behavior_specs]
        self.behavior_specs = [self.env.behavior_specs[b] for b in self.behavior_names]
        self.behavior_name = self.behavior_names[0]
        self.behavior_spec = self.behavior_specs[0]
        self.action_shape = (self.behavior_spec.action_shape,)
        self.state_shape = [s[0] for s in self.behavior_spec.observation_shapes]
        rays = 101
        steps = 5
        self.state_shape[0] -= rays*(steps-1)
        self.state_shape = (sum(self.state_shape),)
        print("ACTION SHAPE:",self.action_shape)
        print("State SHAPE:",self.state_shape)

    def step(self,actions=None):
        if(actions is not None):
            self.env.set_actions(self.behavior_name, actions)
            self.env.step()

        ds,ts =  self.env.get_steps(self.behavior_name)
        actors = {}

        print("DS:")
        print(ds.agent_id)
        print([o.shape for o in ds.obs])
        print(ds.reward)

        rays = 101
        steps = 5
        for i,ID in enumerate(ds.agent_id):
            print(i,ID)
            raycast = ds.obs[0][i][rays*(steps-1):]
            positions = ds.obs[1][i]
            state = np.concatenate((raycast,positions)).flatten()
            actors[ID] = {'obs':state,'reward':ds.reward[i],'done':False}

        for i,ID in enumerate(ts.agent_id):
            raycast = ts.obs[0][i][rays*(steps-1):]
            positions = ts.obs[1][i]
            state = np.concatenate((raycast,positions)).flatten()
            actors[ID] = {'obs':state,'reward':ts.reward[i],'done':True}

        return actors

    def reset(self):
        actors = {}
        ds,ts =  self.env.reset()
        for i,ID in enumerate(ds.agent_id):
            actors[ID] = {'obs':ds.obs[i],'reward':ds.reward[i],'done':False}

        for i,ID in enumerate(ts.agent_id):
            actors[ID] = {'obs':ts.obs[i],'reward':ts.reward[i],'done':True}

        return actors


# env_fn = lambda : UnityEnvWrapper()

# ppo(env_fn)

