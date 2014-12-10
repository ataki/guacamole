# attack mode
DELETE = 1
REVERSE = 2
TARGETED = 3

# graph type
ADVOGATO_GRAPH = 1
RANDOM_GRAPH = 2
LARGE_RANDOM_GRAPH = 3
SMALL_RANDOM_GRAPH =  4
WIKI_GRAPH = 5

# property type
IN_DEGREE_DISTRIBUTION = 1
OUT_DEGREE_DISTRIBUTION = 2
LOCAL_CLUSTERING_COEFFICIENT = 3
GLOBAL_CLUSTERING_COEFFICIENT = 4
DISTANCES = 5
SEED_DISTANCES = 6
ESTIMATED_DIAMETER = 7
PERCENT_BY_DIRECTIONAL_EDGE = 8
AVERAGE_OUT_DEGREE_PER_LEVEL = 9
TRIADS = 10

# sampling result type
TRUE_POSITIVES = 1
MAX_SCC_SIZE = 2
SEED_SCC_SIZE = 3

# output type
ROC = 1
PROPERTIES = 2 # overlay plot clustering coefficient and seed distance, global clustering coefficient, estimated_distance

def print_graph_type(graph_type):
    return {
        ADVOGATO_GRAPH: 'advogato graph',
        RANDOM_GRAPH: 'random graph',
        LARGE_RANDOM_GRAPH: '4x random graph',
        SMALL_RANDOM_GRAPH: '0.25x random graph',
        WIKI_GRAPH: 'wiki graph'
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
        PERCENT_BY_DIRECTIONAL_EDGE: 'Percentage of By-Directional Edges',
        AVERAGE_OUT_DEGREE_PER_LEVEL: 'Average Out-Degree per Distance Level',
        TRIADS: 'Percentage of Triads'
    }[property_mode]

def print_sample_mode(sample_mode):
    return {
        TRUE_POSITIVES: 'true positives',
        MAX_SCC_SIZE: 'max scc size',
        SEED_SCC_SIZE: 'seed scc size'
    }[sample_mode]

def print_output_mode(output_mode):
    return {
        ROC: 'roc',
        PROPERTIES: 'properties'
    }