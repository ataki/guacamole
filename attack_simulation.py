from attack_sampling.py import *
import advogato_trust_metrics as tm

import advogato_trust_metrics as tm

DELETE, REVERSE, TARGETED = 1, 2, 3

def run_attack_simulation(g, seed_v, capacities, attack_mode, compromised_nodes):
    graph = Graph(g)

    for node in compromised_nodes:
        v = graph.vertex(node)

        for e in v.out_edges():
            graph.remove_edge(e)

        if attack_mode == REVERSE:
            for other in graph.vertices():
                if node != other and g.edge(node, other) == None:
                    graph.add_edge(node, other)

        if attack_mode == TARGETED:
            for other in compromised_nodes:
                if node != other:
                    graph.add_edge(node, other)

    return tm.compute_advogato_trust_metrics(graph, seed_v, capacities)