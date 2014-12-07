import metrics

import numpy
from graph_tool.all import *

def _sample_by_distance(distances, sampleSize, sampleTimes):
    # maxDist = max(distances.values())
    # probs = [(float)x/maxDist for x in distances.values()]
    # total = sum(probs)
    # probs = [(float)x/total for x in probs]
        
    # samplesCollection = sampleTimes*[[]]
    # for i in range(0, sampleTimes):
    #     samplesCollection[i] = numpy.random.choice(len(probs), sampleSize, replace=False, p=probs)
        
    # return samplesCollection
    return []

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