import os
import simplejson as json
from matplotlib import pyplot as plt

styls = ['ro-', 'go-', 'bo-', 'ko-']
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
    attack_modes = data_map[graph_type].keys()
    for i, attack_mode in enumerate(attack_modes):
        plt.clf()
        attack_scales = data_map[graph_type][attack_mode]
        for j, attack_scale in enumerate(attack_scales):
            style = styls[j]
            xs, ys = data_map[graph_type][attack_mode][attack_scale]
            plt.plot(xs, ys, style, label="%s compromised nodes" % attack_scale, markerfacecolor="None", markeredgewidth=1, markeredgecolor=style[0])
        plt.plot([0, 1], [0, 1], 'k--')
        outfilename = graph_type.replace(" ", "-").replace(".", "") + "-" + attack_mode.replace(".", "")
        plt.title("%s, %s" % (graph_type, attack_mode))
        plt.legend(loc='lower right', fontsize='medium')
        plt.ylabel("True Positive Rate")
        plt.xlabel("False Positive Rate")
        plt.savefig("%s-roc.png" % outfilename)
