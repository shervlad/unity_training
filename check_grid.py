from unity_env_wrapper import UnityEnvWrapper
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

env = UnityEnvWrapper()

for i in range(10000):
    actors = env.step(np.array([[0]]))

    state = actors[0]['obs']


    bluepoints = (state[0] > 1.1) + 0
    bluegrid = bluepoints.reshape((50,50,50))

    redpoints = ((state[0] > 0.9) + 0) - ((state[0] > 1.1) + 0)
    redgrid = redpoints.reshape((50,50,50))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    ax.set_zlim(0, 50)

    for (grid,color) in [(redgrid,'red'),(bluegrid,'blue')]:
        print(color)
        notEmpty = np.sum(grid) > 5
        z,x,y= grid.nonzero()
        # z*=10
        # x*=10
        # y*=10
        if(notEmpty):
            print(state)
            ax.scatter(x, y, z, zdir='z', s=10, c= color)

    plt.savefig("%s.png"%i)
    # plt.show()
    # plt.close()



