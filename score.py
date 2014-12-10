import os
import simplejson as json
from sklearn.metrics import auc

for filename in os.listdir("logs"):
    path = os.path.join("logs", filename)
    with open(path) as f:
        try:
            data = json.loads(f.read())
        except:
            continue
        config = data["configuration"]
        name = "%s %s %s" % (config.get("graph_type", ""),
                          config.get("attack_mode", ""),
                          config.get("attack_scale", ""))
        try:
            ys = [float(x) for x in data["plot"]["y_axis"]]
            xs = [float(x) for x in data["plot"]["x_axis"]]
            score = auc(xs, ys)
            print "%s: %f" % (name, score)
        except:
            continue
