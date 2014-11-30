from graph_tool.all import *
import sys

seed_color = 3.14
sink_color = 6.25
trusted_color = 1

seed_size = 15
sink_size = 15
trusted_size = 5
untrusted_size = 2

# Modifies the graph, converts all vertices in seeds into one virtual seed vertex.
def virtual_seed_graph(graph, seeds):
    seed_v = graph.add_vertex()
    for v in seeds:
        for out_v in v.out_neighbours():
            graph.add_edge(seed_v, out_v)

    # Clears in- and out- degrees of seeds other than the virtual seed.
    # These original seeds will be isolated in the single-source-sink graph and
    # therefore will not influence the result.
    for v in seeds:
        graph.clear_vertex(graph.vertex(v))

    return seed_v

def distance_to_capacity(dist, capacities, v, seed_v):
    d = min(dist[v], len(capacities) - 1)
    # If v is not the seed, then distance 0 associates to a
    # disconnected node. Always return 1.
    if (d == 0) and (v != seed_v):
        return 1
    return capacities[d]

def init_or_increment(d, k):
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
        self.cap[e.target()] = distance_to_capacity(self.dist, self.capacities, e.target(), self.seed_v)

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
        init_or_increment(self.out_degrees, self.dist[e.source()])
        init_or_increment(self.num_vertices, self.dist[e.target()])

# Graph is directly loaded from .dot file and will
# not be modified.
# Seed is the name of the trust seed.
# Capacities is either
# 1) a list that maps distance-to-seed to
# the assigned capacity
# or
# 2) the total number of vertices to trust.
def compute_advogato_trust_metrics(graph, seed_v, capacities, plot=False):
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
            # edge_caps[inf_e] = float('inf')
            edge_caps[inf_e] = max_cap * 2 # Times 2 just to be safe.

    res = edmonds_karp_max_flow(ss_graph, ss_seed_v, ss_sink_v, edge_caps)

    trusted_v = []
    for v in graph.vertices():
        minus_v = ss_graph.vertex(v)
        sink_e = ss_graph.edge(minus_v, ss_sink_v)
        if res[sink_e] == 0:
            trusted_v += [v]
            # print "%d[%s] is trustworthy." % (v, graph.vp['vertex_name'][v])

    if plot:
        res.a = edge_caps.a - res.a # Actual flow
        p_graph = Graph(graph)
        plot_seed_v = p_graph.vertex(seed_v)
        plot_sink_v = p_graph.add_vertex() # Adds sink.

        # Adds edges to sink.
        for v in p_graph.vertices():
            if v != plot_sink_v:
                p_graph.add_edge(v, plot_sink_v)

        vertex_fill_color = p_graph.new_vertex_property('float')
        vertex_fill_color[plot_seed_v] = seed_color
        vertex_fill_color[plot_sink_v] = sink_color
        vertex_size = p_graph.new_vertex_property('int')
        vertex_size[plot_seed_v] = seed_size
        vertex_size[plot_sink_v] = sink_size
        plot_flows = p_graph.new_edge_property('int')
        for e in ss_graph.edges():
            # This is when edge is from - to sink.
            if e.target() == ss_sink_v:
                source_v = p_graph.vertex(e.source())
                plot_flows[p_graph.edge(source_v, plot_sink_v)] = res[e]
                if res[e] > 0 and source_v != plot_seed_v:
                    vertex_fill_color[source_v] = trusted_color
                    vertex_size[source_v] = trusted_size
                if res[e] == 0 and source_v != plot_seed_v:
                    # vertex_fill_color[source_v] = untrusted_color
                    vertex_size[source_v] = untrusted_size
            else:
                # This is when edge is from - to +.
                # if int(e.source()) + graph.num_vertices() == int(e.target()):
                    # Do something about vertex size.
                # This is an inf edge.
                if int(e.source()) + graph.num_vertices() != int(e.target()):
                    source_v = p_graph.vertex(int(e.source()) - graph.num_vertices())
                    target_v = p_graph.vertex(e.target())
                    plot_flows[p_graph.edge(source_v, target_v)] = res[e]

        graph_draw(p_graph, pos=None, vertex_size=vertex_size, edge_pen_width=prop_to_size(plot_flows, mi=0, ma=5, power=1), vertex_fill_color=vertex_fill_color, output="test_plot.pdf")

    return trusted_v