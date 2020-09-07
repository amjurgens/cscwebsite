from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider, Range1d, RadioButtonGroup
from bokeh.plotting import Figure, output_file, show
import numpy as np

output_file("public_html\escort_distributions.html")


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


def MSP_data(Ts, N=4000, N_trans=100):
    """Calculate and store N points on the simplex, throwing away the first N_trans points."""
    Xs = []
    Ys = []
    Ps = []
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
        Ps.append(Z)
        Xs.append(x)
        Ys.append(y)

    return Xs, Ys, Ps

alpha_Ts = [np.array([[2.73431071e-02, 3.91962466e-01, 1.92405399e-02],
                      [4.74783405e-01, 2.17601974e-02, 2.76643585e-04],
                      [2.23931557e-01, 2.71091756e-03, 2.36095191e-01]]),
            np.array([[0.00184492, 0.13288402, 0.25872353],
                      [0.03912501, 0.31482266, 0.0278933 ],
                      [0.46698011, 0.0101486 , 0.0046992 ]]),
            np.array([[0.09782259, 0.03374265, 0.03643618],
                      [0.0542208 , 0.0650285 , 0.00208948],
                      [0.05327898, 0.00127769, 0.00087775]])]

beta_Ts = [np.array([[0.0500099 , 0.38761941, 0.04250754],
                     [0.46430524, 0.04484055, 0.02494843],
                     [0.2320357 , 0.02720239, 0.24329829]]),
           np.array([[0.00170825, 0.12304039, 0.2395581 ],
                     [0.03622675, 0.2915016 , 0.02582705],
                     [0.4323877 , 0.00939682, 0.0043511 ]]),
           np.array([[0.0905762 , 0.0312431 , 0.0337371 ],
                     [0.05020429, 0.06021139, 0.0019347 ],
                     [0.04933224, 0.00118304, 0.00081273]])]

sarah_Ts = [np.array([[0.48, 0.02, 0.02],
        [0.06, 0.16, 0.02],
        [0.06, 0.02, 0.16]]),
 np.array([[0.16, 0.06, 0.02],
        [0.02, 0.48, 0.02],
        [0.02, 0.06, 0.16]]),
 np.array([[0.16, 0.02, 0.06],
        [0.02, 0.16, 0.06],
        [0.02, 0.02, 0.48]])]


alpha_Xs, alpha_Ys, alpha_Ps = MSP_data(alpha_Ts)
alpha_P0, alpha_P1, alpha_P2 = zip(*alpha_Ps)

beta_Xs, beta_Ys, beta_Ps = MSP_data(beta_Ts)
beta_P0, beta_P1, beta_P2 = zip(*beta_Ps)

sarah_Xs, sarah_Ys, sarah_Ps = MSP_data(sarah_Ts)
sarah_P0, sarah_P1, sarah_P2 = zip(*sarah_Ps)

source = ColumnDataSource(data=dict(x=sarah_Xs, y=sarah_Ys,
                                    p0=sarah_P0, p1=sarah_P1, p2=sarah_P2,
                                    alpha_p0=alpha_P0, alpha_p1=alpha_P1, alpha_p2=alpha_P2,
                                    beta_p0=beta_P0, beta_p1=beta_P1, beta_p2=beta_P2,
                                    sarah_p0=sarah_P0, sarah_p1=sarah_P1, sarah_p2=sarah_P2))

p = Figure(tools="reset, box_zoom", height=800, width=850)
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


p.circle('x', 'y', source=source, size=2, color='navy', alpha=0.8)
# p.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

button_callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var x = data['x'];
    var y = data['y'];
    var P0 = data['p0'];
    var P1 = data['p1'];
    var P2 = data['p2'];

    if (cb_obj.active == 0) {
        P0 = data['alpha_p0'];
        P1 = data['alpha_p1'];
        P2 = data['alpha_p2'];

        for (var i = 0; i < x.length; i++) {
        x[i] =  Math.sqrt(2) * (P0[i] + P1[i] / 2);
        y[i] = P1[i] * Math.sqrt(6) * 0.5 };

    } else if (cb_obj.active == 1) {
        P0 = data['beta_p0'];
        P1 = data['beta_p1'];
        P2 = data['beta_p2'];
        
        for (var i = 0; i < x.length; i++) {
        x[i] =  Math.sqrt(2) * (P0[i] + P1[i] / 2);
        y[i] = P1[i] * Math.sqrt(6) * 0.5 };

    } else if (cb_obj.active == 2) {
        P0 = data['sarah_p0'];
        P1 = data['sarah_p1'];
        P2 = data['sarah_p2'];
        
        for (var i = 0; i < x.length; i++) {
        x[i] =  Math.sqrt(2) * (P0[i] + P1[i] / 2);
        y[i] = P1[i] * Math.sqrt(6) * 0.5 };
    }
    
    source.change.emit();

""")

LABELS = ["Option 1", "Option 2", "Option 3"]

radio_button_group = RadioButtonGroup(labels=LABELS, active=0)
# radio_button_group.js_on_click(CustomJS(code="""
#     console.log('radio_button_group: active=' + this.active, this.toString())
# """))
slider = Slider(start=-4, end=4, value=1, step=.05, title="Beta")

callback = CustomJS(args=dict(source=source, button=radio_button_group, slider=slider), code="""
    var data = source.data;
    var f = slider.value;
    var m = button.active;

    if (m == 0) {
        var x = data['x'];
        var y = data['y'];
        var P0 = data['alpha_p0'];
        var P1 = data['alpha_p1'];
        var P2 = data['alpha_p2'];
    } else if (m == 1) {
        var x = data['x'];
        var y = data['y'];
        var P0 = data['beta_p0'];
        var P1 = data['beta_p1'];
        var P2 = data['beta_p2'];
    } else if (m == 2) {
        var x = data['x'];
        var y = data['y'];
        var P0 = data['sarah_p0'];
        var P1 = data['sarah_p1'];
        var P2 = data['sarah_p2'];
    }

    // var x = data['x'];
    // var y = data['y'];
    // var P0 = data['p0'];
    // var P1 = data['p1'];
    // var P2 = data['p2'];

    for (var i = 0; i < x.length; i++) {
        var P0_beta = P0[i]**f / ( P0[i]**f + P1[i]**f + P2[i]**f ) ;
        var P1_beta = P1[i]**f / ( P0[i]**f + P1[i]**f + P2[i]**f ) ;

        x[i] =  Math.sqrt(2) * (P0_beta + P1_beta / 2);
        y[i] = P1_beta * Math.sqrt(6) * 0.5 ;
    }

    source.change.emit();
""")



slider.js_on_change('value', callback)
radio_button_group.js_on_change('active', button_callback)

layout = column(radio_button_group, slider, p)

show(layout)