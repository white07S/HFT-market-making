import numpy as np
import matplotlib.pyplot as pp;

from utils import (
    MM_Model_Parameters,
    AS3P_Finite_Difference_Solver,
)



lambda_m = 50  # Number of market order arrivals per minute on the bid
lambda_p = 50  # Number of market order arrivals per minute on the ask
kappa_m = 100  # Decay parameter for "fill rate" on the bid
kappa_p = 100  # Decay parameter for "fill rate" on the ask
delta = 0
phi = 0.000001 # running inventory penalty parameter (try changing me!)
alpha = 0.0001 # terminal inventory penalty parameter (try changing me!)
q_min = -25    # largest allowed short position
q_max = 25     # largest allowed long position
cost = 0.005   # trading cost per market order
rebate = 0.0025

# We solve the model for 5 minute chunks. T
T = 5 # minutes
n = 5*60 # one step per second


parameters = MM_Model_Parameters(lambda_m, lambda_p ,kappa_m, kappa_p, delta,
                                   phi, alpha, q_min, q_max, T, cost, rebate)
    
impulses, model = AS3P_Finite_Difference_Solver.solve(parameters, N_steps=n)


# Plot the value function
Y = model.q_grid
X = model.t_grid
X, Y = np.meshgrid(X,Y)
f = pp.figure(figsize=[5, 4]);
pp3d = pp.axes(projection="3d", elev=20, azim=50);
pp3d.set_title("Value function");
pp3d.set_xlabel("Minute");
pp3d.set_ylabel("Inventory");
pp3d.set_zlabel("Value");
pp3d.plot_surface(X, Y, model.h, cmap='magma');


 # Plot the impulse regions
from matplotlib import colors
import matplotlib.patches as mpatches
mycolors = ['white', 'blue', 'red']
cmap = colors.ListedColormap(mycolors)
f, ax = pp.subplots(figsize=[4, 4])
ax.imshow(impulses, cmap=cmap, aspect='auto')
ax.set_xticks([0, 0.5*n, n])
ax.set_xticklabels([0, int(0.5*n), n],fontsize=8);
ax.set_yticks(np.arange(0, len(model.q_grid), 2));
ax.set_yticklabels(model.q_grid[::2],fontsize=8);
ax.set_ylabel('Inventory')
ax.set_xlabel('Second')


# Plot the ask spread for continuation region
f, ax = pp.subplots(figsize=[5, 4])
for q in range(3, -4, -1):
    ax.plot(model.l_p[q], label=f'q={q}')
ax.set_title("Ask to mid spread")
pp.legend()

# Plot the bid spread for continuation region

    

