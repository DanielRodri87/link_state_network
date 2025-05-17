"""
Neighbor Router Management Module

This module handles the management and monitoring of neighboring routers in the network,
including status verification and connectivity checks.
"""

import subprocess
import json
import os
from typing import Dict, List, Tuple, Any

class VizinhosManager:
    """
    Manager for handling neighboring router relationships and status.
    
    This class maintains the state of neighboring routers and provides methods
    for checking their connectivity and updating their status.
    
    Attributes:
        ROTEADOR_ID (str): Unique identifier for this router
        VIZINHOS (Dict): Dictionary of neighbor routers with their IPs and costs
        vizinhos_inativos (List[str]): List of currently inactive neighbors
    """
    
    def __init__(self):
        """Initialize the neighbor manager with router configuration from environment."""
        self.ROTEADOR_ID = os.getenv("ROTEADOR_ID")
        self.VIZINHOS = json.loads(os.getenv("VIZINHOS"))
        self.vizinhos_inativos = []
        
    def verifica_tcp(self, target_ip: str) -> bool:
        """
        Verify TCP connectivity to a target IP address.
        
        Args:
            target_ip: IP address to check connectivity
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            ping_result = subprocess.run(
                f"ping -c 1 -W 0.1 {target_ip}",
                shell=True,
                check=True,
                text=True,
                capture_output=True
            )
            return ping_result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def verifica_roteadores_ativos(self, lsa_database: Dict[str, Any]) -> bool:
        """
        Verify active status of all routers in the LSA database.
        
        Args:
            lsa_database: Database containing router information
            
        Returns:
            bool: True if all routers are active, False otherwise
        """
        for router_id, router_data in list(lsa_database.items()):
            router_status = self.verifica_tcp(router_data["ip"])
            status_msg = "ativo" if router_status else "inativo"
            print(f"[{self.ROTEADOR_ID}] Roteador {router_id} {status_msg}.")
            
            if not router_status:
                return False
        return True
    
    def atualiza_status_vizinhos(self) -> None:
        """
        Update status of all neighboring routers.
        
        Checks connectivity to all neighbors and updates the inactive neighbors list.
        """
        self.vizinhos_inativos = []
        
        for router_id, (router_ip, _) in self.VIZINHOS.items():
            router_status = self.verifica_tcp(router_ip)
            status_msg = "ativo" if router_status else "inativo"
            print(f"[{self.ROTEADOR_ID}] Roteador vizinho {router_id} {status_msg}.")
            
            if not router_status:
                self.vizinhos_inativos.append(router_id)