import matplotlib.pyplot as plt
import numpy as np
import csv

def plot():
    X = []
    Y = []
    with open('metrics.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            X.append(int(row[0]))
            Y.append(float(row[3]))

    fig, ax = plt.subplots()

    (a,b) = np.polyfit(X,Y,1)

    yy = a*np.array(X) + b
    plt.plot(X,Y)
    plt.plot(X,yy)
    # filename = './pusher_results/plots/pi_' + str(epoch)
    # ax.scatter([env.goal[0]],[env.goal[1]])
    # ax.scatter([env.init[0]],[env.init[1]], c='red')
    # ax.scatter([obj_pos[0]],[obj_pos[1]], c='green')
    # plt.savefig(filename, bbox_inches='tight')
    plt.show()
    plt.close()

plot()