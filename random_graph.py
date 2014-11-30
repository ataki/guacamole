import heapq
import math
import random

import advogato_trust_metrics as tm

from graph_tool.all import *

def remove_negative_edges(graph, sample_rate=1.0):
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

def compute_seed_trust(graph, v):
    eprop = graph.edge_properties['label']
    num_pos_edges, num_neg_edges = 0, 0
    # graph is undirected, so out_edges is equivalent of in_edges.
    for e in v.out_edges():
        if eprop[e] == '+':
            num_pos_edges += 1
        if eprop[e] == '-':
            num_neg_edges += 1

    return (float(num_pos_edges) / float(num_pos_edges + num_neg_edges)) * math.sqrt(num_pos_edges)
    # return (float(num_pos_edges) / float(num_pos_edges + num_neg_edges)) * num_pos_edges
    # return num_pos_edges - num_neg_edges

def locate_seed_vertex(graph, num_seeds):
    seeds = []
    for v in graph.vertices():
        v_trust = compute_seed_trust(graph, v)
        if len(seeds) < num_seeds:
            heapq.heappush(seeds, (v_trust, v))
        else:
            heapq.heappushpop(seeds, (v_trust, v))
    
    assert len(seeds) == num_seeds
    return [v for v_trust, v in seeds]

graph_file = 'data/random/random.dot'
full_graph = load_graph(graph_file)
graph = remove_negative_edges(full_graph, 0.5)

seeds = locate_seed_vertex(full_graph, 4)
seed_v = tm.virtual_seed_graph(graph, seeds)
capacities = [800 * len(seeds), 200, 200, 50, 12, 4, 2, 1]

trusted_v = tm.compute_advogato_trust_metrics(graph, seed_v, capacities)
print len(trusted_v)