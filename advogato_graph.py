import advogato_trust_metrics as tm

from graph_tool.all import *

def locate_seed_vertex(graph, seeds):
    seed_vs = []
    for v in graph.vertices():
        if graph.vp['vertex_name'][v] in seeds:
            seed_vs.append(v)
    return seed_vs

graph_file = 'data/advogato-daily/advogato-graph-latest.dot'
# graph_file = 'data/test/test_advogato.dot'
graph = load_graph(graph_file)

seeds = locate_seed_vertex(graph, ['raph', 'miguel', 'federico', 'alan'])
seed_v = tm.virtual_seed_graph(graph, seeds)
capacities = [800 * len(seeds), 200, 200, 50, 12, 4, 2, 1]

trusted_v = tm.compute_advogato_trust_metrics(graph, seed_v, capacities)
print len(trusted_v)