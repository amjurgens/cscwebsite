# myapp.py

from random import random
import numpy as np

from bokeh.layouts import column
from bokeh.models import Button, Range1d, RadioButtonGroup
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc


def closure(Z):
    """Given a point on the n-simplex Z return the L-1 norm."""
    Z = np.array(Z)
    Z = Z/float(np.sum(Z))
    if any(Z < 0):
        return None
    else:
        return Z


def prob(Z, T):
    """Return the probability of map T given a point Z on the n-simplex."""
    Z = closure(Z)
    return np.sum(np.matmul(Z, T))


def evolve(Z, T, n=1):
    """Given a matrix T, evolve a point Z on the n-simplex and return it."""
    Z = closure(Z)

    for i in range(n):
        prob_T = prob(Z, T)
        if prob_T != 0.0:
            Z = np.matmul(Z, T)/prob_T
        else:
            Z = closure([1]*len(Z))
            Z = np.matmul(Z, T)/prob(Z, T)
    return Z


def MSP_data(Ts, N=2000, N_trans=100):
    """Calculate and store N points on the simplex, throwing away the first N_trans points."""
    Xs = []
    Ys = []
    M = len(Ts[0])
    N_matrices = range(len(Ts))

    Z = [1/3., 1/3., 1/3.]
    for n in range(N_trans):
        p = [prob(Z, T) for T in Ts]
        T = Ts[np.random.choice(N_matrices, p=p)]
        Z = evolve(Z, T)
    for n in range(N):
        p = [prob(Z, T) for T in Ts]
        T = Ts[np.random.choice(N_matrices, p=p)]
        Z = evolve(Z, T)
        x = np.sqrt(2)*(Z[0] + Z[1]/2.0)
        y = Z[1]*np.sqrt(6.0)/2.0

        Xs.append(x)
        Ys.append(y)

    return Xs, Ys


def perturb_matrix(seed_Ts, p=0.95, e=0.05):
    """Perturb a seed matrix set to try and find a new, slightly different attractor."""
    M = len(seed_Ts[0])
    Ts = []
    for T in seed_Ts:
        Ts.append(np.array([[x + np.random.choice([0, e], p=[p, 1-p]) for x in row] for row in T]))
    k = np.array([[1/sum(x)]*M for x in sum(Ts)])
    k = (k.reshape(M, M))
    Ts = [np.multiply(k, T) for T in Ts]
    return Ts


# create a plot and style its properties
p = figure(tools="reset, box_zoom", height=800, width=850)
p.grid.grid_line_color = None
p.axis.visible = False
p.grid.grid_line_color = None
p.axis.visible = False
p.y_range = Range1d(-.25, 1.35)
p.x_range = Range1d(-.15, 1.55)

# plot simplex
left_corner = [0.0, 0.0]
right_corner = [np.sqrt(2), 0.0]
top_corner = [np.sqrt(2)/2.0, np.sqrt(6)/2.0]

p.line([left_corner[0], top_corner[0]], [left_corner[1], top_corner[1]], color='black', width=2)
p.line([right_corner[0], top_corner[0]], [right_corner[1], top_corner[1]], color='black', width=2)
p.line([left_corner[0], right_corner[0]], [left_corner[1], right_corner[1]], color='black', width=2)


# add a data renderer to our plot (no data yet)
r = p.circle(x=[], y=[], size=2, fill_color=(255,255,255), alpha=0.8)

i = 0

ds = r.data_source

Ts = [np.array([[2.73431071e-02, 3.91962466e-01, 1.92405399e-02],
        [4.74783405e-01, 2.17601974e-02, 2.76643585e-04],
        [2.23931557e-01, 2.71091756e-03, 2.36095191e-01]]),
 np.array([[0.00184492, 0.13288402, 0.25872353],
        [0.03912501, 0.31482266, 0.0278933 ],
        [0.46698011, 0.0101486 , 0.0046992 ]]),
 np.array([[0.09782259, 0.03374265, 0.03643618],
        [0.0542208 , 0.0650285 , 0.00208948],
        [0.05327898, 0.00127769, 0.00087775]])]

# create a callback that will add a number in a random location
def callback():
    global Ts

    Ts = perturb_matrix(Ts)

    # BEST PRACTICE --- update .data in one step with a new dict
    Xs, Ys = MSP_data(Ts)
    color = tuple(np.random.choice(range(256), size=3))
    r.glyph.line_color = 'navy'
    r.glyph.fill_color = color
    ds.data = dict(x=Xs, y=Ys)


# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))


