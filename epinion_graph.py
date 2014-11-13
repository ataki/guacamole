from graph_tool.all import *
import advogato_trust_metrics as tm

def locate_seed_vertex(graph, seed):
    for v in graph.vertices():
        if graph.vp['vertex_name'][v] == seed:
            return v

graph_file = 'data/epinions/epinions.dot'
seed = '353'

graph = load_graph(graph_file)
# capacities = graph.num_vertices()
capacities = [800, 200, 200, 50, 12, 4, 2, 1]

seed_v = locate_seed_vertex(graph, seed)
trusted_v = tm.compute_advogato_trust_metrics(graph, seed_v, capacities, True)
print len(trusted_v)

