"""
Route Management Module

This module implements routing algorithms and path management for network routing,
including Dijkstra's shortest path algorithm and route table management.
"""

import heapq
from typing import Dict, List, Set, Optional, Any

class GerenciadorDeRotas:
    """
    Manager for network routing and path calculations.
    
    This class handles route calculations, path finding, and maintains routing tables
    using Dijkstra's algorithm for shortest path computation.
    
    Attributes:
        lsdb (Dict): Link State Database containing network topology
        inativos (List[str]): List of inactive routers to exclude from calculations
        tabela_de_rotas (Dict): Routing table for all network paths
    """
    
    def __init__(self, link_state_db: Dict[str, Any], inactive_routers: List[str] = None):
        """
        Initialize the route manager.
        
        Args:
            link_state_db: Link State Database with network topology
            inactive_routers: List of inactive router IDs
        """
        self.lsdb = link_state_db
        self.inativos = inactive_routers or []
        self.tabela_de_rotas = {}

    def set_inativos(self, inactive_routers: List[str]) -> None:
        """Update the list of inactive routers."""
        self.inativos = inactive_routers

    def _gerar_grafo(self) -> Dict[str, Dict[str, int]]:
        """
        Generate a graph representation from the LSDB.
        
        Returns:
            Dict containing network graph with costs
        """
        network_graph = {}
        for router_id, router_data in self.lsdb.items():
            if router_id in self.inativos:
                continue
            active_neighbors = {
                neighbor_id: info['custo']
                for neighbor_id, info in router_data['vizinhos'].items()
                if neighbor_id not in self.inativos
            }
            network_graph[router_id] = active_neighbors
        return network_graph

    def dijkstra(self, source: str) -> Dict[str, str]:
        """
        Implement Dijkstra's shortest path algorithm.
        
        Args:
            source: Source router ID
            
        Returns:
            Dict mapping destinations to next hops
        """
        network_graph = self._gerar_grafo()
        
        print(f"[Dijkstra] Inativos: {self.inativos}")
        
        if source not in network_graph:
            print(f"[Dijkstra] Origem {source} não encontrada no grafo.")
            return {}

        distances = {router: float('inf') for router in network_graph}
        previous = {router: None for router in network_graph}
        distances[source] = 0
        priority_queue = [(0, source)]

        while priority_queue:
            current_cost, current_router = heapq.heappop(priority_queue)
            
            if current_cost > distances[current_router]:
                continue

            for neighbor, weight in network_graph[current_router].items():
                path_cost = distances[current_router] + weight
                if neighbor in distances and path_cost < distances[neighbor]:
                    distances[neighbor] = path_cost
                    previous[neighbor] = current_router
                    heapq.heappush(priority_queue, (path_cost, neighbor))

        routing_table = {}
        for destination in network_graph:
            if destination == source or distances[destination] == float('inf'):
                continue
            current = destination
            while previous[current] != source:
                current = previous[current]
                if current is None:
                    break
            if current:
                routing_table[destination] = current

        return {dest: next_hop for dest, next_hop in routing_table.items() 
                if next_hop != dest}

    def calcular_todas_rotas(self) -> None:
        """Calculate routes for all routers in the network."""
        self.tabela_de_rotas = {
            router: self.dijkstra(router)
            for router in self.lsdb.keys()
        }

    def calcular_caminho(self, source: str, destination: str, 
                        current_path: Optional[List[str]] = None) -> Optional[List[str]]:
        """
        Calculate complete path between source and destination.
        
        Args:
            source: Source router ID
            destination: Destination router ID
            current_path: Current path being built (used in recursion)
            
        Returns:
            List of router IDs forming the path, or None if no path exists
        """
        if current_path is None:
            current_path = [source]
        
        if source == destination:
            return current_path

        if (source not in self.tabela_de_rotas or 
            destination not in self.tabela_de_rotas[source]):
            return None
        
        next_hop = self.tabela_de_rotas[source][destination]
        updated_path = current_path + [next_hop]
        
        return self.calcular_caminho(next_hop, destination, updated_path)

    def exibir_caminhos(self) -> None:
        """Display all calculated paths in the network."""
        for source in self.tabela_de_rotas:
            print(f"✅ Roteador: {source}")
            for destination in self.tabela_de_rotas[source]:
                path = self.calcular_caminho(source, destination)
                if path:
                    complete_path = " ➜ ".join(path)
                    next_hop = self.tabela_de_rotas[source][destination]
                    print(f"Destino: {destination}\tPróximo Salto: {next_hop}\t"
                          f"Caminho Completo: {complete_path}")
                else:
                    print(f"Destino: {destination}\tCaminho inválido")
            print()

if __name__ == "__main__":
    
    # Exemplo de uso
    lsdb = {
    'roteador1': {
        'id': 'roteador1',
        'ip': '172.21.0.2',
        'vizinhos': {
            'roteador5': {'ip': '172.21.4.2', 'custo': 10},
            'roteador2': {'ip': '172.21.1.2', 'custo': 10}
        },
        'seq': 1
    },
    'roteador2': {
        'id': 'roteador2',
        'ip': '172.21.1.2',
        'vizinhos': {
            'roteador1': {'ip': '172.21.0.2', 'custo': 10},
            'roteador3': {'ip': '172.21.2.2', 'custo': 10}
        },
        'seq': 2
    },
    'roteador3': {
        'id': 'roteador3',
        'ip': '172.21.2.2',
        'vizinhos': {
            'roteador2': {'ip': '172.21.1.2', 'custo': 10},
            'roteador4': {'ip': '172.21.3.2', 'custo': 10}
        },
        'seq': 3
    },
    'roteador4': {
        'id': 'roteador4',
        'ip': '172.21.3.2',
        'vizinhos': {
            'roteador3': {'ip': '172.21.2.2', 'custo': 10},
            'roteador5': {'ip': '172.21.4.2', 'custo': 10}
        },
        'seq': 4
    },
    'roteador5': {
        'id': 'roteador5',
        'ip': '172.21.4.2',
        'vizinhos': {
            'roteador4': {'ip': '172.21.3.2', 'custo': 10},
            'roteador1': {'ip': '172.21.0.2', 'custo': 10}
        },
        'seq': 5
    }
}

    # Lista de roteadores inativos para teste
    inativos = ['roteador3']

    # print("Vizinhos acessíveis:", verifica_vizinhos("roteador1", lsdb, inativos))
    
    lista_caminhos = {}
    roteador = GerenciadorDeRotas(lsdb,inativos)
    # Atualiza as rotas levando em consideração os inativos
    # for roteador in lsdb.keys():
    #     # print(roteador)
    #     lista_caminhos[roteador] = dijkstra(roteador, lsdb, inativos)
    
    print(roteador.dijkstra('roteador4'))
    # print(roteador.dijkstra('roteador4', lsdb, []))
