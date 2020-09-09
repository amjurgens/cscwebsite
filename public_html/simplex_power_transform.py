from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider, Range1d, Label
from bokeh.plotting import Figure, output_file, show
import numpy as np
from bokeh.palettes import magma

output_file("simplex_power_transform.html")

def power_transform(P, beta):
    beta_P = [p**beta for p in P]
    return beta_P/np.sum(beta_P)

def closure(Z):
    """Given a point on the n-simplex Z return the L-1 norm."""
    Z = np.array(Z)
    Z = Z/float(np.sum(Z))
    if any(Z < 0):
        return None
    else:
        return Z

p = Figure(tools="", height=800, width=850)
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

p.line([left_corner[0], top_corner[0]], [left_corner[1], top_corner[1]], color='black', line_width=2)
p.line([right_corner[0], top_corner[0]], [right_corner[1], top_corner[1]], color='black', line_width=2)
p.line([left_corner[0], right_corner[0]], [left_corner[1], right_corner[1]], color='black', line_width=2)

left_label = Label(x=left_corner[0], y=left_corner[1],
                        text='Pr(0, 0, 1)', render_mode='css',
                        x_offset=-5, y_offset=-30, text_align='center')
right_label = Label(x=right_corner[0], y=right_corner[1],
                        text='Pr(1, 0, 0)', render_mode='css',
                        x_offset=5, y_offset=-30, text_align='center')
top_label = Label(x=top_corner[0], y=top_corner[1],
                        text='Pr(0, 1, 0)', render_mode='css',
                        x_offset=0, y_offset=20, text_align='center')
p.add_layout(left_label)
p.add_layout(right_label)
p.add_layout(top_label)

# add points

N_points = 1000

simplex_points = [closure(list(np.random.rand(3))) for i in range(N_points)]
P0, P1, P2 = zip(*simplex_points)
Xs = [np.sqrt(2)*(Z[0] + Z[1]/2.0) for Z in simplex_points]
Ys = [Z[1]*np.sqrt(6.0)/2.0 for Z in simplex_points]

# colors = [np.random.choice(range(256), size=3) for i in range(N_points)]
colors = magma(256) + magma(256) + magma(256) + magma(256)

source = ColumnDataSource(data=dict(x=Xs, y=Ys, color=colors[:N_points],
                                    P0=P0, P1=P1, P2=P2) )

p.scatter('x', 'y', source=source, color='color', alpha=1.0, size= 4)
p.circle(0.7071067811865476, 0.40824829046386296, color='black', size=10)

# add slider
beta_max = 10
slider = Slider(start=-beta_max, end=beta_max, value=1, step=.1, title="Beta")

# slider javascript
slider_callback = CustomJS(args=dict(source=source, slider=slider), code="""
    var data = source.data;
    var f = slider.value;

    var x = data['x'];
    var y = data['y'];
    var P0 = data['P0'];
    var P1 = data['P1'];
    var P2 = data['P2']

    for (var i = 0; i < x.length; i++) {
        var P0_beta = P0[i]**f / ( P0[i]**f + P1[i]**f + P2[i]**f ) ;
        var P1_beta = P1[i]**f / ( P0[i]**f + P1[i]**f + P2[i]**f ) ;

        x[i] = Math.sqrt(2) * (P0_beta + P1_beta / 2);
        y[i] = P1_beta * Math.sqrt(6) * 0.5 ;
    }

    source.change.emit();
""")


slider.js_on_change('value', slider_callback)

layout = column(slider, p)

show(layout)