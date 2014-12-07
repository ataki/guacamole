from trust_graph import TrustGraph
from params import *
import graphs
from logging import SimulationLogger

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

def _prepare_roc_plot(trusted_nodes, results):
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

        x.append(xe + (x[-1] if len(x) > 0 else 0))
        y.append(ye + (y[-1] if len(y) > 0 else 0))

    x = [(float(e)/false_positives if false_positives > 0 else 0) for e in x]
    y = [(float(e)/true_positives if true_positives > 0 else 0) for e in y]
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
    x, y = _prepare_roc_plot(trusted_nodes, results)

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

num_experiments = 100
run_simulation(RANDOM_GRAPH, 1, DELETE, edge_sample_rate=0.5, comment='Random graph has 2x edges, so edge_sample_rate is 50\%')