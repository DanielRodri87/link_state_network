import yaml
import networkx as nx
import matplotlib.pyplot as plt
import os
import json

def ler_topologia():
    # Lê o arquivo docker-compose.yml
    compose_path = os.path.join(os.path.dirname(__file__), '../../../docker-compose.yml')
    with open(compose_path, 'r') as file:
        compose = yaml.safe_load(file)
    
    G = nx.Graph()
    
    # Extrai conexões dos roteadores
    for service, config in compose['services'].items():
        if service.startswith('roteador'):
            G.add_node(service)
            if 'environment' in config:
                for env in config['environment']:
                    if 'VIZINHOS' in env:
                        vizinhos = json.loads(env.split('=')[1].strip())
                        for vizinho in vizinhos.keys():
                            G.add_edge(service, vizinho)
    
    return G

def identificar_topologia(G):
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    # Verifica se é anel
    if num_edges == num_nodes and nx.is_connected(G):
        graus = [d for n, d in G.degree()]
        if all(d == 2 for d in graus):
            return "Anel"
    
    # Verifica se é estrela
    if num_edges == num_nodes - 1:
        graus = [d for n, d in G.degree()]
        if graus.count(1) == num_nodes - 1 and graus.count(num_nodes - 1) == 1:
            return "Estrela"
    
    # Verifica se é malha completa
    if num_edges == (num_nodes * (num_nodes - 1)) // 2:
        return "Malha Completa"
    
    # Verifica se é barramento
    if nx.is_connected(G) and all(d <= 2 for n, d in G.degree()):
        return "Barramento"
    
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