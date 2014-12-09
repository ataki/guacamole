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

def _subsampling(graph_type, edge_sample_rate, minimal_sample_rate, sample_interval):
    logger = SimulationLogger()
    logger.add_subsampling_configuration(graph_type, edge_sample_rate, minimal_sample_rate, sample_interval)

    print 'Initializing graph...'
    if graph_type == ADVOGATO_GRAPH:
        graph = graphs.advogato_trust_graph(edge_sample_rate)
    else:
        graph = graphs.random_trust_graph(edge_sample_rate, graph_type)

    deleted_percentages = []
    results = []

    for rate in range(100, int(args.minimal_sample_rate*100)-1, int(-args.sample_interval*100)):
        rate /= 100.0
        deleted_percentages.append(1.0 - rate)
        print "Sampling at %f..." % rate
        attacked_graph = graph.get_sampled_graph(rate)
        results.append(attacked_graph.get_trusted_nodes())

    trusted_nodes = graph.get_trusted_nodes()
    true_positives = [_true_positives(result, trusted_nodes) for result in results]

    for (rate, true_positive) in zip(deleted_percentages, true_positives):
        logger.add_sample(rate, true_positive)

    print 'Logging...'
    logger.write()
    print 'Plotting...'
    logger.plot_subsampling('%s: Subsampling' % print_graph_type(graph_type),
        deleted_percentages, true_positives,
        'percentage of edges removed', 'true positives')

FIGURE_DIR = 'subsampling/'
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--graph', type=int, default=1)
    parser.add_argument('-m', '--minimal_sample_rate', type=float, default=0.0)
    parser.add_argument('-i', '--sample_interval', type=float, default=0.1)
    parser.add_argument('-c', '--comments', default='')
    args = parser.parse_args()

    edge_sample_rate = 1.0 if (args.graph == ADVOGATO_GRAPH) else 0.5
    _subsampling(args.graph, edge_sample_rate, args.minimal_sample_rate, args.sample_interval)