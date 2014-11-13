from graph_tool.all import *
import advogato_trust_metrics as tm

graph_file = 'data/epinions/epinions.dot', 
capacities = [800, 200, 200, 50, 12, 4, 2, 1]

graph = load_graph(graph_file)
tm.compute_advogato_trust_metrics(graph, seed, capacities)

