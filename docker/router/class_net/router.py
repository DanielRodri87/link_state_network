"""
Router Application Module

This module implements the main router application that coordinates all routing functionality
including LSA management, neighbor monitoring, and route updates.
"""

import threading
import os
from typing import List, Dict, Any
from class_net.neighbor_manager import VizinhosManager
from class_net.lsa_manager import LSAManager
from class_net.route_update import AtualizadorDeRotas
from class_net.route_manager import GerenciadorDeRotas

class RoteadorApp:
    """
    Main router application class that coordinates all routing functionality.
    
    This class manages the Link State Database (LSDB), coordinates various managers
    for network operations, and handles threading for concurrent operations.
    
    Attributes:
        lsdb (Dict): Link State Database storing network topology
        stop_event (threading.Event): Event to control thread execution
        vizinhos_manager (VizinhosManager): Manager for neighbor operations
        lsa_manager (LSAManager): Manager for LSA operations
        gerenciador_de_rotas (GerenciadorDeRotas): Manager for route calculations
        rota_manager (AtualizadorDeRotas): Manager for route updates
        active_threads (List[threading.Thread]): List of running threads
    """
    
    def __init__(self):
        """Initialize router application components and managers."""
        self.lsdb: Dict[str, Any] = {}
        self.stop_event = threading.Event()

        # Initialize component managers
        self.vizinhos_manager = VizinhosManager()
        self.lsa_manager = LSAManager(self.vizinhos_manager)
        self.gerenciador_de_rotas = GerenciadorDeRotas(
            self.lsdb, 
            self.vizinhos_manager.vizinhos_inativos
        )
        self.rota_manager = AtualizadorDeRotas(self.gerenciador_de_rotas)
        self.active_threads: List[threading.Thread] = []

    def atualizar_tabela(self) -> None:
        """
        Monitor and update routing table based on network changes.
        
        Continuously checks router status and recalculates routes when needed.
        """
        while not self.stop_event.is_set():
            if not self.vizinhos_manager.verifica_roteadores_ativos(self.lsdb):
                self.rota_manager.recalcular_rotas(
                    self.vizinhos_manager.vizinhos_inativos
                )
            self.stop_event.wait(0.1)

    def monitorar_vizinhos(self) -> None:
        """
        Monitor neighbor router status and update routes accordingly.
        
        Continuously checks neighbor status and triggers route recalculation.
        """
        while not self.stop_event.is_set():
            self.vizinhos_manager.atualiza_status_vizinhos()
            self.rota_manager.recalcular_rotas(
                self.vizinhos_manager.vizinhos_inativos
            )
            self.stop_event.wait(0.5)

    def iniciar_threads(self) -> None:
        """
        Initialize and start all router operation threads.
        
        Creates and starts threads for LSA operations, table updates,
        and neighbor monitoring.
        """
        self.active_threads = [
            threading.Thread(target=self.lsa_manager.enviar_lsa, 
                           args=(self.stop_event,)),
            threading.Thread(target=self.lsa_manager.receber_lsa, 
                           args=(self.lsdb, self.stop_event)),
            threading.Thread(target=self.atualizar_tabela),
            threading.Thread(target=(self.monitorar_vizinhos))
        ]

        for thread in self.active_threads:
            thread.daemon = True
            thread.start()

        self.stop_event.wait()

    def parar(self) -> None:
        """
        Stop all router operations and threads gracefully.
        
        Sets the stop event and waits for all threads to complete.
        """
        self.stop_event.set()
        for thread in self.active_threads:
            thread.join()
            
if __name__ == "__main__":
    router_application = RoteadorApp()
