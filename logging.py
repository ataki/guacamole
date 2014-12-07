from params import *

import datetime
import json

import Gnuplot
Gnuplot.GnuplotOpts.default_term = 'png'

LOG_DIR = 'logs/'
PLOT_DIR = 'plots/'

class SimulationLogger:
    def __init__(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.log = LOG_DIR + ('log-%s' % current_time)
        self.plot = PLOT_DIR + ('plot-%s' % current_time)
        open(self.log, 'a')
        self.data = {}
        self.comment = ''

    def add_comment(self, comment):
        self.comment = comment
        self.data['comment'] = self.comment

    def add_configuration(self, graph_type, attack_scale, attack_mode, edge_sample_rate, percent_edge_compromised):
        self.data['configuration'] = {
            'graph_type': print_graph_type(graph_type),
            'attack_scale': attack_scale,
            'attack_mode': print_attack_mode(attack_mode),
            'edge_sample_rate': edge_sample_rate,
            'percent_edge_compromised': percent_edge_compromised
        }

    def add_plotting_data(self, x, y):
        self.data['plot'] = {
            'x_axis': x,
            'y_axis': y
        }

    def add_trusted_nodes(self, trusted_nodes):
        self.data['trusted_nodes'] = trusted_nodes

    def add_trusted_nodes_after_attack(self, attack_id, trusted_nodes):
        if 'add_trusted_nodes_after_attack' not in self.data:
            self.data['add_trusted_nodes_after_attack'] = {}
        self.data['add_trusted_nodes_after_attack'][attack_id] = trusted_nodes

    def write(self):
        with open(self.log, 'a') as log:
             json.dump(self.data, log, indent=4)

    def plot_roc(self, title, x, y):
        g = Gnuplot.Gnuplot()
        g.title(title)
        g('set output \'%s\'' % self.plot)
        g('set grid')
        g.xlabel('false positives')
        g.ylabel('true positives')
        data = Gnuplot.Data(x, y, with_='linespoints pt 6')
        g.plot(data)