from unity_env_wrapper import UnityEnvWrapper
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

env = UnityEnvWrapper()

for i in range(10000):
    actors = env.step(np.array([[0]]))

    state = actors[0]['obs']


    print("TOTAL NONZERO: ", np.sum((state[0] > 0 + 0)))
    redpoints = ((state[0] > 0.9) + 0) - ((state[0] > 1.1) + 0)
    redgrid = redpoints.reshape((20,20,20))

    bluepoints = (state[0] > 1.1) + 0
    bluegrid = bluepoints.reshape((20,20,20))

    notEmpty = np.sum(bluepoints + redpoints) > 5
    if(not notEmpty):
        continue

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_zlim(0, 20)

    for (grid,color) in [(redgrid,'red'),(bluegrid,'blue')]:
        z,x,y= grid.nonzero()
        # z*=10
        # x*=10
        # y*=10
        print(state)
        ax.scatter(x, y, z, zdir='z', s=10, c= color)

    plt.savefig("%s.png"%i)
    # plt.show()
    # plt.close()



