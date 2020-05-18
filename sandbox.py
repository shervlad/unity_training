from mlagents_envs.environment import UnityEnvironment, DecisionSteps
import numpy as np

# This is a non-blocking call that only loads the environment.
print(1)
env = UnityEnvironment(file_name=None, seed=1, worker_id=0, side_channels=[])
# Start interacting with the evironment.
print(2)
env.reset()
print(3)
print(4)
behavior_names = [b for b in env.behavior_specs]
behavior_name = behavior_names[0]
print(behavior_names)
ds,ts = env.get_steps(behavior_name)
print("Agent ID:",ds.agent_id)
print(5)
bs = env.behavior_specs[behavior_name]
print(bs)
action_size = bs.action_size
print("action size: ",action_size)

for i in range(200):
    # print(i)
    ds,ts = env.get_steps(behavior_names[0])
    agent_ids = ds.agent_id
    # print("DECISION STEPS: ")
    print(agent_ids)
    print(ds.reward)
    for o in ds.obs:
        print(o.shape)
    # print("TERMINAL STEPS: ")
    # print(ts.agent_id)
    # print(ts.reward)
    # print(ts.obs)
    # for i in range(len(ts.obs)):
    #     print(ts.obs[i].flatten())
    actions = np.random.rand(len(agent_ids),action_size)*2 - 1
    # env.set_action_for_agent(behavior_names[0],agent_ids[0],actions[0])
    env.set_actions(behavior_names[0], actions)
    env.step()
    # else:
    #     env.reset()
print(6)
env.close()
# for i in range(100):

#     action = np.random.rand(action_size)
