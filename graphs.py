from trust_graph import TrustGraph

import heapq
import math
import random
from graph_tool.all import *

# Modifies the graph, converts all vertices in seeds into one virtual seed vertex.
def _transform_virtual_seed(graph, seeds):
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

def _seed_score(graph, v):
    eprop = graph.edge_properties['label']
    num_pos_edges, num_neg_edges = 0, 0
    # graph is undirected, so out_edges is equivalent of in_edges.
    for e in v.out_edges():
        if eprop[e] == '+':
            num_pos_edges += 1
        if eprop[e] == '-':
            num_neg_edges += 1

    return (float(num_pos_edges) / float(num_pos_edges + num_neg_edges)) * math.sqrt(num_pos_edges)

def _get_seeds(graph, num_seeds):
    seeds = []
    for v in graph.vertices():
        v_trust = _seed_score(graph, v)
        if len(seeds) < num_seeds:
            heapq.heappush(seeds, (v_trust, v))
        else:
            heapq.heappushpop(seeds, (v_trust, v))
    
    assert len(seeds) == num_seeds
    return [v for v_trust, v in seeds]


def _normalize_random_graph(graph, sample_rate=1.0):
    g = Graph()
    g.add_vertex(graph.num_vertices())
    eprop = graph.edge_properties['label']
    for e in graph.edges():
        if eprop[e] == '+':
            if random.random() < sample_rate:
                g.add_edge(e.source(), e.target())
            if random.random() < sample_rate:
                g.add_edge(e.target(), e.source())
    return g

def _get_seeds_by_name(graph, seeds):
    seed_vs = []
    for v in graph.vertices():
        if graph.vp['vertex_name'][v] in seeds:
            seed_vs.append(v)
    return seed_vs

def random_trust_graph():
    num_seeds = 4
    random_graph = load_graph('data/random/random.dot')

    graph = _normalize_random_graph(random_graph, 0.5)
    seeds = _get_seeds(random_graph, num_seeds)

    seed_v = _transform_virtual_seed(graph, seeds)
    capacities = [800 * num_seeds, 200, 200, 50, 12, 4, 2, 1]
    return TrustGraph(graph, seed_v, capacities)

def advogato_trust_graph():
    graph = load_graph('data/advogato-daily/advogato-graph-latest.dot')
    seeds = _get_seeds_by_name(graph, ['raph', 'miguel', 'federico', 'alan'])
    seed_v = _transform_virtual_seed(graph, seeds)
    capacities = [800 * 4, 200, 200, 50, 12, 4, 2, 1]
    return TrustGraph(graph, seed_v, capacities)