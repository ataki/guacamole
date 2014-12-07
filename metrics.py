from graph_tool.all import *

def _distance_to_capacity(dist, capacities, v, seed_v):
    d = min(dist[v], len(capacities) - 1)
    # If v is not the seed, then distance 0 associates to a
    # disconnected node. Always return 1.
    if (d == 0) and (v != seed_v):
        return 1
    return capacities[d]

def _init_or_increment(d, k):
    if k in d:
        d[k] = d[k] + 1
    else:
        d[k] = 1

# Subclass of BFSVisitor.
# Assigns a distance to each vertex during BFS.
class ManualCapacityVisitor(BFSVisitor):
    def __init__(self, dist, cap, capacities, seed_v):
        self.dist = dist
        self.cap = cap
        self.capacities = capacities
        self.seed_v = seed_v
        self.cap[seed_v] = capacities[0]

    def tree_edge(self, e):
        self.dist[e.target()] = self.dist[e.source()] + 1
        self.cap[e.target()] = _distance_to_capacity(self.dist, self.capacities, e.target(), self.seed_v)

class AutoCapacityVisitor(BFSVisitor):
    def __init__(self, dist, out_degrees, num_vertices, init_cap):
        self.dist = dist
        self.out_degrees = out_degrees
        self.num_vertices = num_vertices
        self.init_cap = init_cap

        # Adds the seed to l=0.
        self.num_vertices[0] = 1

    def tree_edge(self, e):
        self.dist[e.target()] = self.dist[e.source()] + 1
        _init_or_increment(self.out_degrees, self.dist[e.source()])
        _init_or_increment(self.num_vertices, self.dist[e.target()])

# Graph is directly loaded from .dot file and will
# not be modified.
# Seed is the name of the trust seed.
# Capacities is either
# 1) a list that maps distance-to-seed to
# the assigned capacity
# or
# 2) the total number of vertices to trust.
def advogato_trust_metric_results(graph, seed_v, capacities):
    # Computes distance to seed.
    # Seed vertex AND disconnected vertices all have distance 0.
    dist = graph.new_vertex_property('int')
    cap = graph.new_vertex_property('int')
    if type(capacities) is list:
        max_cap = capacities[0]
        bfs_search(graph, seed_v, ManualCapacityVisitor(dist, cap, capacities, seed_v))
    else:
        out_degrees = {}
        num_vertices = {}
        bfs_search(graph, seed_v, AutoCapacityVisitor(dist, out_degrees, num_vertices, capacities))
        max_dist = max(num_vertices.keys())
        max_cap = capacities
        capacities = [max_cap]
        for l in range(1, max_dist):
            capacities.append(capacities[l - 1] / max(out_degrees[l - 1] / num_vertices[l - 1], 1))
        for v in graph.vertices():
            cap[v] = capacities[dist[v] - 1]

        print capacities

    # Creates a new directed graph with single sink.
    ss_graph = Graph()
    ss_graph.add_vertex(graph.num_vertices() * 2 + 1)
    ss_seed_v = ss_graph.vertex(seed_v)
    ss_sink_v = ss_graph.vertex(graph.num_vertices() * 2)
    edge_caps = ss_graph.new_edge_property('int')
    for v in graph.vertices():
        minus_v = ss_graph.vertex(v)
        plus_v = ss_graph.vertex(graph.num_vertices() + int(v))

        # Adds edge from - to +, and edge from - to sink.
        flow_e = ss_graph.add_edge(minus_v, plus_v)
        edge_caps[flow_e] = cap[v] - 1
        sink_e = ss_graph.add_edge(minus_v, ss_sink_v)
        edge_caps[sink_e] = 1

        for n_v in v.out_neighbours():
            n_minus_v = ss_graph.vertex(n_v)
            inf_e = ss_graph.add_edge(plus_v, n_minus_v)
            edge_caps[inf_e] = max_cap * 2 # Times 2 just to be safe.

    res = edmonds_karp_max_flow(ss_graph, ss_seed_v, ss_sink_v, edge_caps)

    trusted_v = []
    for v in graph.vertices():
        minus_v = ss_graph.vertex(v)
        sink_e = ss_graph.edge(minus_v, ss_sink_v)
        if res[sink_e] == 0:
            trusted_v += [v]

    return trusted_v
