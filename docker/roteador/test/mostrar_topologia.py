import yaml
import networkx as nx
import matplotlib.pyplot as plt
import os
import json

def ler_topologia():
    # Lê o arquivo config.yaml gerado
    config_path = os.path.join(
    os.path.dirname(__file__), 
    '../../../gera_yml/config.yaml')
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    G = nx.Graph()
    
    # Adiciona roteadores como nós
    for roteador in config['routers']:
        G.add_node(roteador['id'])
    
    # Adiciona conexões entre os roteadores
    for roteador in config['routers']:
        for vizinho in roteador['neighbors']:
            G.add_edge(roteador['id'], vizinho['id'])
    
    return G
def identificar_topologia(G):
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    # Verifica se é anel
    if num_edges == num_nodes and nx.is_connected(G) and all(d == 2 for n, d in G.degree()):
        return "Anel"
    
    # Verifica se é estrela
    if num_edges == num_nodes - 1:
        degrees = [d for n, d in G.degree()]
        if degrees.count(1) == num_nodes - 1 and degrees.count(num_nodes - 1) == 1:
            return "Estrela"
    
    # Verifica se é malha completa
    if num_edges == (num_nodes * (num_nodes - 1)) // 2:
        return "Malha Completa"
    
    # Verifica se é linha (grau máximo 2 e conectado)
    if nx.is_connected(G) and max([d for n, d in G.degree()]) <= 2:
        return "Linha"
    
    # Verifica se é árvore (grafo acíclico)
    if nx.is_tree(G):
        return "Árvore"
    
    return "Customizada"

def mostrar_topologia():
    G = ler_topologia()
    tipo_topologia = identificar_topologia(G)
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2000, font_size=16, font_weight='bold')
    
    plt.title(f"Topologia da Rede: {tipo_topologia}", pad=20, fontsize=16)
    plt.show()

if __name__ == "__main__":
    mostrar_topologia()