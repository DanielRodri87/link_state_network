"""
Route Update Module

This module handles the updating of routing tables and system routing configurations
for network routers. It manages route calculations and system-level route updates.
"""

import subprocess
import os
from typing import Dict
from class_net.manipulation import Manipulacao
from class_net.route_manager import GerenciadorDeRotas

class AtualizadorDeRotas:
    """
    Manager for updating system routing tables.
    
    This class handles the updating of system routing tables based on
    calculated routes and manages route recalculation when network changes occur.
    
    Attributes:
        ROTEADOR_ID (str): Unique identifier for this router
        gerenciador_de_rotas (GerenciadorDeRotas): Route calculation manager
    """
    
    def __init__(self, gerenciador_de_rotas: GerenciadorDeRotas):
        """
        Initialize the route updater.
        
        Args:
            gerenciador_de_rotas: Route calculation manager instance
        """
        self.ROTEADOR_ID = os.getenv("ROTEADOR_ID")
        self.gerenciador_de_rotas = gerenciador_de_rotas

    def atualizar_rota(self, routing_table: Dict[str, str]) -> None:
        """
        Update system routing table with new routes.
        
        Args:
            routing_table: Dictionary mapping destinations to next hops
        """
        for destination, next_hop in routing_table.items():
            destination_ip = self.gerenciador_de_rotas.lsdb[destination]['ip']
            next_hop_ip = self.gerenciador_de_rotas.lsdb[next_hop]['ip']
            
            destination_subnet = Manipulacao.extrair_subnet_roteador_ip(destination_ip)
            gateway_ip = Manipulacao.extrair_ip_roteadores_ip(next_hop_ip)
            
            route_command = f"ip route replace {destination_subnet} via {gateway_ip}"
            print(f"[{self.ROTEADOR_ID}] Executando: {route_command}")
            
            command_result = subprocess.run(route_command, shell=True, capture_output=True, text=True)
            
            if command_result.returncode != 0:
                print(f"[{self.ROTEADOR_ID}] Erro: {command_result.stderr.strip()}")
            else:
                print(f"[{self.ROTEADOR_ID}] Rota atualizada: {command_result.stdout.strip()}")

    def recalcular_rotas(self, inactive_routers: list) -> None:
        """
        Recalculate and update routes based on network changes.
        
        Args:
            inactive_routers: List of currently inactive routers
        """
        self.gerenciador_de_rotas.set_inativos(inactive_routers)
        
        routing_table = self.gerenciador_de_rotas.dijkstra(self.ROTEADOR_ID)
        if routing_table:
            print(f"[{self.ROTEADOR_ID}] Nova tabela de rotas:")
            for destination, next_hop in routing_table.items():
                print(f"  {destination} → via {next_hop}")
            self.atualizar_rota(routing_table)
        else:
            print(f"[{self.ROTEADOR_ID}] Nenhuma rota encontrada.")