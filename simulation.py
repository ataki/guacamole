import graphs
from logging import SimulationLogger
from params import *
from trust_graph import TrustGraph

import argparse

def _test_attack_resistance(graph, num_experiments, attack_scale, attack_mode):
    results = []
    percent_edge_compromised = []
    trusted_nodes = graph.get_trusted_nodes()
    
    for i in range(num_experiments):
        print "Test attack resistance, attack %d..." % (i + 1)
        attacked_graph, edges_modified = graph.get_attacked_graph(attack_scale, attack_mode)
        results.append(attacked_graph.get_trusted_nodes())
        percent_edge_compromised.append(float(edges_modified) / graph.graph.num_edges())

    return results, percent_edge_compromised

def _accumulate_list(l):
    s = 0
    for i in range(len(l)):
        l[i] += s
        s = l[i]

def _prepare_roc_plot(trusted_nodes, results, sorted=True):
    # false_positives are nodes that are trusted after the attack, but should not be trusted
    # false_negatives are nodes that are not trusted, but should be trusted
    false_positives, true_positives = 0, 0
    x, y = [], []
    for trusted_nodes_after_attack in results:
        xe, ye = 0, 0
        for node in trusted_nodes_after_attack:
            if node in trusted_nodes:
                true_positives += 1
                ye += 1
            else:
                false_positives += 1
                xe += 1

        # x.append(xe + (x[-1] if len(x) > 0 else 0))
        # y.append(ye + (y[-1] if len(y) > 0 else 0))
        x.append(xe)
        y.append(ye)
    sorted_yx = zip(y, x)
    sorted_yx.sort(reverse=True)
    sorted_x = [x for (y, x) in sorted_yx]
    sorted_y = [y for (y, x) in sorted_yx]
    _accumulate_list(sorted_x)
    _accumulate_list(sorted_y)

    x = [(float(e)/false_positives if false_positives > 0 else 0) for e in sorted_x]
    y = [(float(e)/true_positives if true_positives > 0 else 0) for e in sorted_y]
    return x, y

def run_simulation(graph_type, attack_scale, attack_mode, edge_sample_rate=1.0, comment=''):
    logger = SimulationLogger()
    logger.add_comment(comment)
    
    print "Initializing graph..."
    if graph_type == RANDOM_GRAPH:
        graph = graphs.random_trust_graph(edge_sample_rate)
    if graph_type == ADVOGATO_GRAPH:
        graph = graphs.advogato_trust_graph(edge_sample_rate)

    trusted_nodes = graph.get_trusted_nodes()
    results, percent_edge_compromised = _test_attack_resistance(graph, num_experiments, attack_scale, attack_mode)
    x, y = _prepare_roc_plot(trusted_nodes, results, True)

    logger.add_configuration(graph_type, attack_scale, attack_mode, edge_sample_rate, percent_edge_compromised)
    logger.add_trusted_nodes(trusted_nodes)
    logger.add_plotting_data(x, y)
    for i in range(num_experiments):
        logger.add_trusted_nodes_after_attack('attack-%d' % (i + 1), results[i])

    print "Writing to log..."
    logger.write()
    plot_title = '%s: %s-attack with scale %d' % (print_graph_type(graph_type), print_attack_mode(attack_mode), attack_scale)
    print "Plotting..."
    logger.plot_roc(plot_title, x, y)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scale', type=int, default=1)
    # DELETE, REVERSE, TARGETED = 1, 2, 3
    parser.add_argument('-m', '--mode', type=int, default=1)
    # RANDOM_GRAPH, ADVOGATO_GRAPH = 1, 2
    parser.add_argument('-g', '--graph', type=int, default=1)
    parser.add_argument('-r', '--sample', type=float, default=1.0)
    parser.add_argument('-e', '--num_experiments', type=int, default=100)
    parser.add_argument('-c', '--comments', default='')
    args = parser.parse_args()

    num_experiments = args.num_experiments
    run_simulation(args.graph, args.scale, args.mode, edge_sample_rate=args.sample, comment=args.comments)