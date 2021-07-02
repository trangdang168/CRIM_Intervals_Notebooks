"""
This file contains the visualizations I'm working on.
"""
import pandas as pd
import networkx as nx
from pyvis.network import Network
import re

def add_nodes_to_net(melodic_interval_column):
    networks_dict = {'all': Network(directed=True, notebook=True)}
    melodic_interval_column = melodic_interval_column.astype(str)
    networks_dict['all'].add_node('all', color='red', shape='circle', level=0)

    # create nodes from the patterns
    for node in melodic_interval_column:
        nodes = re.sub(r'([+-])(?!$)', r'\1,', node).split(",")
        group = nodes[0]

        if not group in networks_dict:
            networks_dict[group] = Network(directed=True, notebook=True)

        prev_node = 'all'
        for i in range(1, len(nodes)):
            node_id = "".join(node for node in nodes[:i])
            # add to its own family network
            networks_dict[group].add_node(node_id, group=group, physics=False, level=i)
            if prev_node != "all":
                networks_dict[group].add_edge(prev_node, node_id)

            # add to the big network
            networks_dict['all'].add_node(node_id, group=group, physics=False, level=i)
            networks_dict['all'].add_edge(prev_node, node_id)
            prev_node = node_id

    return networks_dict

def main():
    df_observations = pd.read_csv('observations.csv')
    networks_dict = add_nodes_to_net(df_observations['mt_fg_int'])
    print(networks_dict.keys())
    networks_dict['all'].show('all_fuga.html')
    networks_dict['4-'].show('family.html')
main()