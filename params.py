# attack mode
DELETE, REVERSE, TARGETED = 1, 2, 3

# graph type
RANDOM_GRAPH, ADVOGATO_GRAPH = 1, 2

# property type
IN_DEGREE_DISTRIBUTION = 1
OUT_DEGREE_DISTRIBUTION = 2
LOCAL_CLUSTERING_COEFFICIENT = 3
GLOBAL_CLUSTERING_COEFFICIENT = 4
DISTANCES = 5
SEED_DISTANCES = 6

def print_graph_type(graph_type):
    return {
        RANDOM_GRAPH: 'random graph',
        ADVOGATO_GRAPH: 'advogato graph'
    }[graph_type]

def print_attack_mode(attack_mode):
    return {
        DELETE: 'delete',
        REVERSE: 'reverse',
        TARGETED: 'targeted'
    }[attack_mode]