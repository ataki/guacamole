import os
import simplejson as json
from matplotlib import pyplot as plt

styls = ['r-', 'g-', 'b-', 'k-']
data_map = {}

for filename in os.listdir("logs"):
    path = os.path.join("logs", filename)
    with open(path) as f:
        try:
            data = json.loads(f.read())
        except:
            continue
        config = data["configuration"]

        pk = config["graph_type"]
        graph_type_data = data_map.get(pk, {})
        if "attack_mode" not in config:
            continue
        else:
            sk = config["attack_mode"]
        attack_mode_data = graph_type_data.get(sk, {})

        if "attack_scale" not in config:
            continue
        else:
            tk = config["attack_scale"]

        try:
            ys = [float(x) for x in data["plot"]["y_axis"]]
            xs = [float(x) for x in data["plot"]["x_axis"]]
            attack_mode_data[tk] = (xs, ys)
        except:
            print "error with ", path
            continue

        graph_type_data[sk] = attack_mode_data
        data_map[pk] = graph_type_data

for graph_type in data_map.keys():
    plt.clf()
    attack_modes = data_map[graph_type].keys()
    for i, attack_mode in enumerate(attack_modes):
        attack_scales = data_map[graph_type][attack_mode]
        style = styls[i]
        for attack_scale in attack_scales:
            xs, ys = data_map[graph_type][attack_mode][attack_scale]
            plt.plot(xs, ys, style, label="%s %f" % (attack_mode, attack_scale))
    graph_type = graph_type.replace(" ", "-").replace(".", "")
    plt.title(graph_type)
    plt.legend(loc='lower right', fontsize='small')
    plt.savefig("%s-roc.png" % graph_type)
