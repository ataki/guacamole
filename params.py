# attack mode
DELETE, REVERSE, TARGETED = 1, 2, 3

# graph type
ADVOGATO_GRAPH = 1
RANDOM_GRAPH = 2
LARGE_RANDOM_GRAPH = 3
SMALL_RANDOM_GRAPH =  4

# property type
IN_DEGREE_DISTRIBUTION = 1
OUT_DEGREE_DISTRIBUTION = 2
LOCAL_CLUSTERING_COEFFICIENT = 3
GLOBAL_CLUSTERING_COEFFICIENT = 4
DISTANCES = 5
SEED_DISTANCES = 6
ESTIMATED_DIAMETER = 7
PERCENT_BY_DIRECTIONAL_EDGE = 8

def print_graph_type(graph_type):
    return {
        ADVOGATO_GRAPH: 'advogato graph',
        RANDOM_GRAPH: 'random graph',
        LARGE_RANDOM_GRAPH: '4x random graph',
        SMALL_RANDOM_GRAPH: '0.25x random graph'
    }[graph_type]

def print_attack_mode(attack_mode):
    return {
        DELETE: 'delete',
        REVERSE: 'reverse',
        TARGETED: 'targeted'
    }[attack_mode]

def print_property_type(property_mode):
    return {
        IN_DEGREE_DISTRIBUTION: 'In-Degree Distribution',
        OUT_DEGREE_DISTRIBUTION: 'Out-Degree Distribution',
        LOCAL_CLUSTERING_COEFFICIENT: 'Local Clustering Coefficient',
        GLOBAL_CLUSTERING_COEFFICIENT: 'Global Clustering Coefficient',
        DISTANCES: 'Diameters Estimated at Each Vertex',
        SEED_DISTANCES: 'Shortest Path Lengths from Seed',
        ESTIMATED_DIAMETER: 'Diameter',
        PERCENT_BY_DIRECTIONAL_EDGE: 'Percentage of By-Directional Edges'
    }[property_mode]