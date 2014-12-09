import metrics
from params import *

import numpy

from graph_tool.all import *

def _sample_by_distance(distances, sample_size, sample_times):
    probs = [float(x) / sum(distances.values()) for x in distances.values()]

    sample = []
    for i in range(sample_times):
        sample.append(numpy.random.choice(distances.keys(), sample_size, replace=False, p=probs))
        
    return sample

# Subclass of BFSVisitor.
# Assigns a distance to each vertex during BFS.
class DistanceVisitor(BFSVisitor):
    def __init__(self, distances, seed):
        self.distances = distances
        self.distances[seed] = 0

    def tree_edge(self, e):
        self.distances[e.target()] = self.distances[e.source()] + 1

class TrustGraph:
    def __init__(self, graph, seed, capacities):
        self.graph = graph
        self.seed = seed
        self.capacities = capacities
        self.distances = {}
        bfs_search(self.graph, self.seed, DistanceVisitor(self.distances, self.seed))
        self.trusted_nodes = None

    def get_trusted_nodes(self):
        if self.trusted_nodes == None:
            self.trusted_nodes = metrics.advogato_trust_metric_results(self.graph, self.seed, self.capacities)
        return self.trusted_nodes

    def sample_compromised_nodes(self, sample_size):
        return _sample_by_distance(self.distances, sample_size, 1)[0]

    def get_attacked_graph(self, attack_scale, attack_mode):
        attacked_graph = Graph(self.graph)
        compromised_nodes = self.sample_compromised_nodes(attack_scale)
        edges_modified = 0

        for v in compromised_nodes:
            for e in attacked_graph.vertex(v).out_edges():
                edges_modified += 1
                attacked_graph.remove_edge(e)

            if attack_mode == REVERSE:
                for w in attacked_graph.vertices():
                    if v != w and self.graph.edge(v, w) == None:
                        edges_modified += 1
                        attacked_graph.add_edge(v, w)

            if attack_mode == TARGETED:
                for w in compromised_nodes:
                    if v != w:
                        if self.graph.edge(v, w) != None:
                            edges_modified -= 1
                        else:
                            edges_modified += 1
                        attacked_graph.add_edge(v, w)

        return TrustGraph(attacked_graph, self.seed, self.capacities), edges_modified