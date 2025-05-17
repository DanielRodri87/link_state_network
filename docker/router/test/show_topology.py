import yaml
import networkx as nx
import matplotlib.pyplot as plt
import os

def ler_topologia():
    # Lê o arquivo config.yaml gerado
    config_path = os.path.join(
        os.path.dirname(__file__), 
        '../../../gera_yml/config.yaml'
    )
    
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

    # Verifica se é Totalmente Conectada
    if num_edges == (num_nodes * (num_nodes - 1)) // 2:
        return "Totalmente Conectada"

    # Verifica se é Anel
    if nx.is_connected(G) and all(d == 2 for n, d in G.degree()):
        return "Anel"

    # Verifica se é Estrela
    degrees = [d for n, d in G.degree()]
    if degrees.count(1) == num_nodes - 1 and degrees.count(num_nodes - 1) == 1:
        return "Estrela"

    # Verifica se é Linha (grau máximo 2, dois nós com grau 1 e resto grau 2)
    if nx.is_connected(G):
        degree_vals = [d for n, d in G.degree()]
        if degree_vals.count(1) == 2 and all(d <= 2 for d in degree_vals):
            return "Linha"

    # Verifica se é Árvore (conectado e sem ciclos)
    if nx.is_tree(G):
        return "Árvore"

    return "Customizada"

def mostrar_topologia():
    G = ler_topologia()
    tipo_topologia = identificar_topologia(G)
    
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2000, font_size=16, font_weight='bold')
    
    plt.title(f"Topologia da Rede: {tipo_topologia}", pad=20, fontsize=16)
    plt.show()

if __name__ == "__main__":
    mostrar_topologia()
