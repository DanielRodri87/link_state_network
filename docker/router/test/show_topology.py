"""
Network Topology Visualization Module

This module provides functionality to visualize and identify network topologies
from YAML configuration files using NetworkX and Matplotlib.
"""

import yaml
import networkx as nx
import matplotlib.pyplot as plt
import os
from typing import Dict, Any

def ler_topologia() -> nx.Graph:
    """
    Read and parse network topology from configuration file.
    
    Returns:
        nx.Graph: NetworkX graph representing the network topology
    """
    # Fix path resolution to config.yaml
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        'generate_compose',
        'config.yaml'
    )
    
    with open(config_path, 'r') as config_file:
        network_config = yaml.safe_load(config_file)
    
    topology_graph = nx.Graph()
    
    # Add routers as nodes
    for router in network_config['routers']:
        topology_graph.add_node(router['id'])
    
    # Add connections between routers
    for router in network_config['routers']:
        for neighbor in router['neighbors']:
            topology_graph.add_edge(router['id'], neighbor['id'])
    
    return topology_graph

def identificar_topologia(topology_graph: nx.Graph) -> str:
    """
    Identify the type of network topology from the graph structure.
    
    Args:
        topology_graph: NetworkX graph representing the network topology
        
    Returns:
        str: Identified topology type
    """
    node_count = topology_graph.number_of_nodes()
    edge_count = topology_graph.number_of_edges()

    # Check for Fully Connected topology
    if edge_count == (node_count * (node_count - 1)) // 2:
        return "Totalmente Conectada"

    # Check for Ring topology
    if (nx.is_connected(topology_graph) and 
        all(degree == 2 for _, degree in topology_graph.degree())):
        return "Anel"

    # Check for Star topology
    degree_counts = [degree for _, degree in topology_graph.degree()]
    if (degree_counts.count(1) == node_count - 1 and 
        degree_counts.count(node_count - 1) == 1):
        return "Estrela"

    # Check for Line topology
    if nx.is_connected(topology_graph):
        node_degrees = [degree for _, degree in topology_graph.degree()]
        if (node_degrees.count(1) == 2 and 
            all(degree <= 2 for degree in node_degrees)):
            return "Linha"

    # Check for Tree topology
    if nx.is_tree(topology_graph):
        return "Árvore"

    return "Customizada"

def mostrar_topologia() -> None:
    """
    Display the network topology visualization using matplotlib.
    
    Reads the topology configuration, identifies the topology type,
    and displays a graphical representation.
    """
    topology_graph = ler_topologia()
    topology_type = identificar_topologia(topology_graph)
    
    # Calculate node positions for visualization
    node_positions = nx.spring_layout(topology_graph, seed=42)
    
    # Create and configure the plot
    plt.figure(figsize=(10, 10))
    nx.draw(
        topology_graph, 
        node_positions, 
        with_labels=True, 
        node_color='lightblue',
        node_size=2000, 
        font_size=16, 
        font_weight='bold'
    )
    
    plt.title(f"Topologia da Rede: {topology_type}", pad=20, fontsize=16)
    plt.show()

if __name__ == "__main__":
    mostrar_topologia()
