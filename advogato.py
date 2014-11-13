from graph_tool.all import *

graph_file = 'data/advogato-daily/advogato-graph-latest.dot'
# graph_file = 'data/test/test_advogato.dot'
graph = load_graph(graph_file)
capacities = [800, 200, 200, 50, 12, 4, 2, 1]

def locate_seed_vertex(graph, seed):
    for v in graph.vertices():
        if graph.vp['vertex_name'][v] == seed:
            return v

def distance_to_capacity(dist, capacities, v, seed):
    d = min(dist[v], len(capacities) - 1)
    # If v is not the seed, then distance 0 associates to a
    # disconnected node. Always return 1.
    if (d == 0) and (v != seed):
        return 1
    return capacities[d]

# Subclass of BFSVisitor.
# Assigns a distance to each vertex during BFS.
class AssignDistanceVisitor(BFSVisitor):
    def __init__(self, dist):
        self.dist = dist

    def tree_edge(self, e):
        self.dist[e.target()] = self.dist[e.source()] + 1

# Graph is directly loaded from .dot file and will
# not be modified.
# Seed is the name of the trust seed.
# Capacities is a list that maps distance-to-seed to
# the assigned capacity.
def compute_advogato_trust_metrics(graph, seed, capacities):
    seed_v = locate_seed_vertex(graph, seed)

    # Computes distance to seed.
    # Seed vertex AND disconnected vertices all have distance 0.
    dist = graph.new_vertex_property('int')
    bfs_search(graph, seed_v, AssignDistanceVisitor(dist))

    # Creates a new directed graph with single sink.
    ss_graph = Graph()
    ss_seed_v = ss_graph.vertex(seed_v)
    ss_sink_v = ss_graph.vertex(graph.num_vertices() * 2)
    ss_graph.add_vertex(graph.num_vertices() * 2 + 1)
    edge_caps = ss_graph.new_edge_property('float')
    for v in graph.vertices():
        minus_v = ss_graph.vertex(v)
        plus_v = ss_graph.vertex(graph.num_vertices() + int(v))

        # Adds edge from - to +, and edge from - to sink.
        flow_e = ss_graph.add_edge(minus_v, plus_v)
        edge_caps[flow_e] = distance_to_capacity(dist, capacities, v, seed_v) - 1.0
        sink_e = ss_graph.add_edge(minus_v, ss_sink_v)
        edge_caps[sink_e] = 1.0

        for n_v in v.out_neighbours():
            n_minus_v = ss_graph.vertex(n_v)
            inf_e = ss_graph.add_edge(plus_v, n_minus_v)
            edge_caps[inf_e] = float('inf')

    residual_edge_caps = edmonds_karp_max_flow(ss_graph, ss_seed_v, ss_sink_v, edge_caps)

    for v in graph.vertices():
        minus_v = ss_graph.vertex(v)
        sink_e = ss_graph.edge(minus_v, ss_sink_v)
        if residual_edge_caps[sink_e] == 0:
            print "%d[%s] is trustworthy." % (v, graph.vp['vertex_name'][v])

ss_graph = compute_advogato_trust_metrics(graph, 'raph', capacities)

