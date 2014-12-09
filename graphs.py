from params import *
from trust_graph import TrustGraph

import argparse
import datetime
import heapq
import math
import numpy
import random

from graph_tool.all import *
import Gnuplot
Gnuplot.GnuplotOpts.default_term = 'png'

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


def _normalize_random_graph(graph, sample_rate):
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

def _sample_edges(graph, sample_rate):
    if sample_rate < 1.0:
        g = Graph()
        g.add_vertex(graph.num_vertices())
        for e in graph.edges():
            if random.random() < sample_rate:
                g.add_edge(e.source(), e.target())
        graph = g

def _get_seeds_by_name(graph, seeds):
    seed_vs = []
    for v in graph.vertices():
        if graph.vp['vertex_name'][v] in seeds:
            seed_vs.append(v)
    return seed_vs

def random_trust_graph(edge_sample_rate, graph_type):
    num_seeds = 4

    if graph_type == RANDOM_GRAPH:
        random_graph = load_graph('data/random/random_1.dot')
        capacities = [800 * num_seeds, 200, 200, 50, 12, 4, 2, 1]
    if graph_type == LARGE_RANDOM_GRAPH:
        random_graph = load_graph('data/random/random_4.dot')
        capacities = [3200 * num_seeds, 800, 800, 200, 48, 16, 8, 4, 2, 1]
    if graph_type == SMALL_RANDOM_GRAPH:
        random_graph = load_graph('data/random/random_0.25.dot')
        capacities = [200 * num_seeds, 50, 50, 12, 4, 2, 1]

    seeds = _get_seeds(random_graph, num_seeds)
    graph = _normalize_random_graph(random_graph, edge_sample_rate)

    seed_v = _transform_virtual_seed(graph, seeds)
    return TrustGraph(graph, seed_v, capacities)

def advogato_trust_graph(edge_sample_rate):
    graph = load_graph('data/advogato-daily/advogato-graph-latest.dot')
    seeds = _get_seeds_by_name(graph, ['raph', 'miguel', 'federico', 'alan'])
    _sample_edges(graph, edge_sample_rate)
    seed_v = _transform_virtual_seed(graph, seeds)
    capacities = [800 * 4, 200, 200, 50, 12, 4, 2, 1]
    return TrustGraph(graph, seed_v, capacities)

FIGURE_DIR = 'figures/'
def plot_prop(title, x, y, log_scale=False):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    g = Gnuplot.Gnuplot()
    g.title(title)
    g('set output \'%s\'' % (FIGURE_DIR + ('plot-%s.png' % current_time)))
    g('set grid')
    if log_scale:
        g('set logscale xy 10')
        g('set format x "10^{%L}"')
        g('set mxtics 10')
        g('set format y "10^{%L}"')
        g('set mytics 10')
    g.xlabel('false positives')
    g.ylabel('true positives')
    data = Gnuplot.Data(x, y, with_='linespoints pt 6')
    g.plot(data)

def get_property(graph_type, edge_sample_rate, property_type, comments):
    print "Initializing graph..."
    if graph_type == ADVOGATO_GRAPH:
        graph = advogato_trust_graph(edge_sample_rate)
    else:
        graph = random_trust_graph(edge_sample_rate, graph_type)
    seed = graph.seed
    graph = graph.graph

    print "Preparing property..."
    if property_type == IN_DEGREE_DISTRIBUTION:
        dd = vertex_hist(graph, "in")
        plot_prop("%s - %s" % (print_property_type(property_type), print_graph_type(graph_type)), dd[1][:-1], dd[0], True)
    if property_type == OUT_DEGREE_DISTRIBUTION:
        dd = vertex_hist(graph, "out")
        plot_prop("%s - %s" % (print_property_type(property_type), print_graph_type(graph_type)), dd[1][:-1], dd[0], True)
    if property_type == LOCAL_CLUSTERING_COEFFICIENT:
        clust = local_clustering(graph)
        x = range(graph.num_vertices())
        y = sorted(clust.get_array(), reverse=True)
        plot_prop("%s - %s" % (print_property_type(property_type), print_graph_type(graph_type)), x, y)
    if property_type == GLOBAL_CLUSTERING_COEFFICIENT:
        print "%s: %f" % (print_property_type(property_type), global_clustering(graph)[0])
    if property_type == DISTANCES:
        diameters = []
        for v in graph.vertices():
            diameters.append(pseudo_diameter(graph, v)[0])
        x = range(graph.num_vertices())
        y = sorted(diameters, reverse=True)
        plot_prop("%s - %s" % (print_property_type(property_type), print_graph_type(graph_type)), x, y)
    if property_type == SEED_DISTANCES:
        distances = shortest_distance(graph, source=seed)
        distances = [(dist if dist < 2147483647 else 0) for dist in distances.get_array()]
        x = range(graph.num_vertices())
        y = sorted(distances, reverse=True)
        plot_prop("%s - %s" % (print_property_type(property_type), print_graph_type(graph_type)), x, y)
    if property_type == ESTIMATED_DIAMETER:
        max_diamater = 0
        for source in numpy.random.choice(range(graph.num_vertices()), 100, replace=False):
            max_diamater = max(max_diamater, pseudo_diameter(graph, source)[0])
        print "%s: %d" % (print_property_type(property_type), max_diamater)
    if property_type == PERCENT_BY_DIRECTIONAL_EDGE:
        num_by_directional_edge = 0
        for e in graph.edges():
            if graph.edge(e.target(), e.source()) != None:
                num_by_directional_edge += 1
        print "%s: %f" % (print_property_type(property_type), float(num_by_directional_edge)/graph.num_edges())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # IN_DEGREE_DISTRIBUTION = 1
    # OUT_DEGREE_DISTRIBUTION = 2
    # LOCAL_CLUSTERING_COEFFICIENT = 3
    # GLOBAL_CLUSTERING_COEFFICIENT = 4
    # DISTANCES = 5
    # SEED_DISTANCES = 6
    # ESTIMATED_DIAMETER = 7
    # PERCENT_BY_DIRECTIONAL_EDGE = 8
    parser.add_argument('-p', '--property', type=int, default=1)
    parser.add_argument('-g', '--graph', type=int, default=1)
    parser.add_argument('-r', '--sample', type=float)
    parser.add_argument('-c', '--comments', default='')
    args = parser.parse_args()

    if args.sample == None:
        args.sample = 1.0 if (args.graph == ADVOGATO_GRAPH) else 0.5

    print 'Sampling at %f' % args.sample

    if args.property == 0:
        for p in range(1, 9):
            get_property(args.graph, args.sample, p, args.comments)
    else:
        get_property(args.graph, args.sample, args.property, args.comments)