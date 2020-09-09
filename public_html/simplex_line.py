from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider, Range1d, RadioButtonGroup, HoverTool, Label
from bokeh.plotting import Figure, output_file, show
import numpy as np

output_file("simplex_line.html")

def power_transform(P, beta):
    beta_P = [p**beta for p in P]
    return beta_P/np.sum(beta_P)

stationary_dist = [.15, .55, .3]
max_beta = 15
betas = np.linspace(-max_beta, max_beta, 1000)
simplex_points = [power_transform(stationary_dist, beta) for beta in betas]
Xs = [np.sqrt(2)*(Z[0] + Z[1]/2.0) for Z in simplex_points]
Ys = [Z[1]*np.sqrt(6.0)/2.0 for Z in simplex_points]

source = ColumnDataSource(data=dict(x=Xs, y=Ys, beta=betas, 
                    Zs=[ '(' + ", ".join([str(round(p,2)) for p in Z]) + ')' for Z in simplex_points]) )

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
LINE = p.line('x', 'y', source=source, color='navy', alpha=1.0, line_width=2, )
p.circle(np.sqrt(2)*(stationary_dist[0] + stationary_dist[1]/2.0),
         stationary_dist[1]*np.sqrt(6.0)/2.0, color='navy', size=10)

p.circle(0.7071067811865476, 0.40824829046386296, color='black', size=10)

h = HoverTool(tooltips = [
    ("Distribution", "@Zs"),
    ("Beta", "@beta")],
    mode='hline',
    renderers=[LINE])

p.add_tools(h)

layout = column(p)

show(layout)