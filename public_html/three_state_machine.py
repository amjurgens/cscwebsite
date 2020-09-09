import math
import numpy as np 
import bezier

from bokeh.io import output_file, show
from bokeh.models import Circle, GraphRenderer, StaticLayoutProvider, LabelSet, ColumnDataSource, MultiLine, HoverTool, TapTool, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral8
from bokeh.plotting import figure

## bezier path 
def get_bezier_points(state_positions, output_angle, input_angle, d, num_points=100):
    state_one, state_two = state_positions
    
    Xs = [state_one[0], d*np.cos(np.radians(output_angle)) + state_one[0], 
          d*np.cos(np.radians(input_angle)) + state_two[0], state_two[0]]
    Ys = [state_one[1], d*np.sin(np.radians(output_angle)) + state_one[1], 
          d*np.sin(np.radians(input_angle)) + state_two[1], state_two[1]]
    nodes = np.asfortranarray([Xs,Ys])
    curve = bezier.Curve(nodes, degree=3)
    return curve.evaluate_multi(np.linspace(0.0, 1.0, num_points))

## output file
output_file('three_state_machine.html')

## number of states 
N = 3
node_indices = list(range(N))


## figure back ground
plot = figure(x_range=(-0.5, 1.5), y_range=(-np.sqrt(3)/2-0.7, 0.5),
              tools='', toolbar_location=None)
plot.grid.grid_line_color = None
plot.axis.visible = False
plot.grid.grid_line_color = None
plot.axis.visible = False

plot.add_tools(HoverTool(tooltips=None), TapTool())

graph = GraphRenderer()

state_size = 60
graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.glyph = Circle(size=state_size, fill_color='white', line_width=4)
graph.node_renderer.selection_glyph = Circle(size=state_size, fill_color='red', line_width=4)
graph.node_renderer.hover_glyph = Circle(size=state_size, fill_color='pink', line_width=4)

graph.edge_renderer.glyph = MultiLine(line_color="black", line_width=2)
graph.edge_renderer.selection_glyph = MultiLine(line_color='pink', line_width=2)
graph.edge_renderer.hover_glyph = MultiLine(line_color='red', line_width=2)


### start of layout code
x = [0, .7, 0.35]
y = [0, 0, -0.5]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)


## add edges

edge_list = np.array([[0,0], [0, 1], [1, 2], [2,1], [2, 0]])
d = 0.35
angle_list = [(145, 215, d), (45, 135, d), (270, 0, d), (90, 205, d), (180, 270, d)]
graph.edge_renderer.data_source.data = dict(start=edge_list[:, 0], end=edge_list[:, 1])

xs, ys = [], []
for edge_path, angles in zip(edge_list, angle_list):
    sx, sy = graph_layout[edge_path[0]]
    ex, ey = graph_layout[edge_path[1]]
    input_angle, output_angle, d = angles
    bezier_xs, bezier_ys = get_bezier_points([[sx, sy], [ex, ey]], input_angle, output_angle, d, num_points=100)
    xs.append(bezier_xs)
    ys.append(bezier_ys)

graph.edge_renderer.data_source.data['xs'] = xs
graph.edge_renderer.data_source.data['ys'] = ys

graph.selection_policy = NodesAndLinkedEdges()
graph.inspection_policy = EdgesAndLinkedNodes()

plot.renderers.append(graph)



source = ColumnDataSource(data=dict(x_pos=x,
                                    y_pos=y,
                                    labels=['σ₀',	'σ₁',	'σ₂']))

# add labels
labels = LabelSet(x='x_pos', y='y_pos', text='labels', level='guide', x_offset=-15, 
                  y_offset=-15, source=source, render_mode='canvas',
                  text_font_size='25pt', text_color='black')
plot.add_layout(labels)

show(plot)