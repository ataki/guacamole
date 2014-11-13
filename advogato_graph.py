from graph_tool.all import *
import advogato_trust_metrics as tm

def locate_seed_vertex(graph, seed):
    for v in graph.vertices():
        if graph.vp['vertex_name'][v] == seed:
            return v

graph_file = 'data/advogato-daily/advogato-graph-latest.dot'
seed = 'raph'
capacities = [800, 200, 200, 50, 12, 4, 2, 1]

graph = load_graph(graph_file)
seed_v = locate_seed_vertex(graph, seed)
ss_graph = tm.compute_advogato_trust_metrics(graph, seed_v, capacities)

