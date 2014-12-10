import graphs
from logging import SimulationLogger
from params import *
from trust_graph import TrustGraph

import argparse
import datetime

def _true_positives(result, trusted_nodes):
    count = 0
    for r in result:
        if r in trusted_nodes:
            count += 1

    return float(count)/len(trusted_nodes)

def _subsampling(graph_type, sample_mode, edge_sample_rate, minimal_sample_rate, sample_interval):
    logger = SimulationLogger()
    logger.add_subsampling_configuration(graph_type, sample_mode, edge_sample_rate, minimal_sample_rate, sample_interval)

    print 'Initializing graph...'
    if graph_type == ADVOGATO_GRAPH:
        graph = graphs.advogato_trust_graph(edge_sample_rate)
    if graph_type == WIKI_GRAPH:
        graph = graphs.wiki_trust_graph(edge_sample_rate)
    if graph_type == RANDOM_GRAPH or graph_type == LARGE_RANDOM_GRAPH or graph_type == SMALL_RANDOM_GRAPH:
        graph = graphs.random_trust_graph(edge_sample_rate, graph_type)

    deleted_percentages = []
    results = []

    for rate in range(100, int(args.minimal_sample_rate*100)-1, int(-args.sample_interval*100)):
        rate /= 100.0
        deleted_percentages.append(1.0 - rate)
        print "Sampling at %f..." % rate
        attacked_graph = graph.get_sampled_graph(rate)
        
        if sample_mode == TRUE_POSITIVES:
            true_positive = _true_positives(attacked_graph.get_trusted_nodes(), graph.get_trusted_nodes())
            results.append(true_positive)
        
        if sample_mode == MAX_SCC_SIZE:
            results.append(attacked_graph.get_max_scc_size())

        if sample_mode == SEED_SCC_SIZE:
            results.append(attacked_graph.get_seed_scc_size())

    for (rate, result) in zip(deleted_percentages, results):
        logger.add_sample(rate, result)

    print 'Logging...'
    logger.write()
    print 'Plotting...'
    logger.plot_subsampling('%s: Subsampling - %s' % (print_graph_type(graph_type), print_sample_mode(sample_mode)),
        deleted_percentages, results,
        'percentage of edges removed', print_sample_mode(sample_mode))

FIGURE_DIR = 'subsampling/'
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--graph', type=int, default=1)
    # TRUE_POSITIVES = 1
    # MAX_SCC_SIZE = 2
    # SEED_SCC_SIZE = 3
    parser.add_argument('-m', '--sample_mode', type=int, default=1)
    parser.add_argument('-r', '--minimal_sample_rate', type=float, default=0.0)
    parser.add_argument('-i', '--sample_interval', type=float, default=0.1)
    parser.add_argument('-c', '--comments', default='')
    args = parser.parse_args()

    edge_sample_rate = 1.0 if (args.graph == ADVOGATO_GRAPH or args.graph == WIKI_GRAPH) else 0.5
    _subsampling(args.graph, args.sample_mode, edge_sample_rate, args.minimal_sample_rate, args.sample_interval)