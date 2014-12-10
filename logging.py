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
        self.plot = PLOT_DIR + ('plot-%s.png' % current_time)
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

    def add_subsampling_configuration(self, graph_type, sample_mode, edge_sample_rate, minimal_sample_rate, sample_interval):
        self.data['configuration'] = {
            'graph_type': print_graph_type(graph_type),
            'sample_mode': print_sample_mode(sample_mode),
            'edge_sample_rate': edge_sample_rate,
            'minimal_sample_rate': minimal_sample_rate,
            'sample_interval': sample_interval
        }

    def add_sample(self, sample_rate, true_positives):
        if 'samples' not in self.data:
            self.data['samples'] = {}
        self.data['samples'][sample_rate] = true_positives

    def add_plotting_data(self, x, y):
        self.data['plot'] = {
            'x_axis': x,
            'y_axis': y
        }

    def add_trusted_nodes(self, trusted_nodes):
        self.data['trusted_nodes'] = [int(node) for node in trusted_nodes]

    def add_trusted_nodes_after_attack(self, attack_id, trusted_nodes):
        if 'add_trusted_nodes_after_attack' not in self.data:
            self.data['add_trusted_nodes_after_attack'] = {}
        self.data['add_trusted_nodes_after_attack'][attack_id] = [int(node) for node in trusted_nodes]

    def add_properties(self, average_global_cc, average_estimated_diameter):
        if 'attacked_graph_property' not in self.data:
            self.data['attacked_graph_property'] = {}
        self.data['attacked_graph_property']['global_cc'] = average_global_cc
        self.data['attacked_graph_property']['estimated_diameter'] = average_estimated_diameter

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

    def plot_subsampling(self, title, x, y, x_label, y_label):
        g = Gnuplot.Gnuplot()
        g.title(title)
        g('set output \'%s\'' % self.plot)
        g('set grid')
        g.xlabel(x_label)
        g.ylabel(y_label)
        data = Gnuplot.Data(x, y, with_='linespoints pt 6')
        g.plot(data)