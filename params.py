# attack mode
DELETE, REVERSE, TARGETED = 1, 2, 3

# graph type
RANDOM_GRAPH, ADVOGATO_GRAPH = 1, 2

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