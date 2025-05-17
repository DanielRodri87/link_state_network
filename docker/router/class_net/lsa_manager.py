"""
Link State Advertisement Manager Module

This module handles the creation, sending, and receiving of Link State Advertisements (LSAs)
in a network routing environment. It manages the flooding of network topology information
between routers.
"""

import socket
import json
import os
from threading import Event
from typing import Dict, Tuple, Any
from class_net.neighbor_manager import VizinhosManager

LSA_PORT = 5000

class LSAManager:
    """
    Manages Link State Advertisements (LSAs) for network routing.
    
    This class handles the creation, transmission, and reception of LSAs,
    maintaining network topology information and sequence numbers.
    
    Attributes:
        ROTEADOR_ID (str): Unique identifier for the router
        ENDERECO_IP (str): IP address of the router
        vizinhos_manager (VizinhosManager): Manager for neighbor relationships
        sequence_number (int): Sequence number for LSA messages
    """
    
    def __init__(self, vizinhos_manager: VizinhosManager):
        """
        Initialize the LSA Manager.
        
        Args:
            vizinhos_manager: Manager instance for handling neighbor relationships
        """
        self.ROTEADOR_ID = os.getenv("ROTEADOR_ID")
        self.ENDERECO_IP = os.getenv("ENDERECO_IP")
        self.vizinhos_manager = vizinhos_manager
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sequence_number = 0

    def enviar_lsa(self, stop_event: Event) -> None:
        """
        Send Link State Advertisements to neighbors.
        
        Continuously sends LSA updates to all active neighbors until stopped.
        
        Args:
            stop_event: Threading event to control the sending loop
        """
        while not stop_event.is_set():
            self.sequence_number += 1
            lsa_data = {
                "id": self.ROTEADOR_ID,
                "ip": self.ENDERECO_IP,
                "vizinhos": {
                    neighbor: {"ip": ip, "custo": cost} 
                    for neighbor, (ip, cost) in self.vizinhos_manager.VIZINHOS.items() 
                    if neighbor not in self.vizinhos_manager.vizinhos_inativos
                },
                "seq": self.sequence_number
            }
            
            encoded_message = json.dumps(lsa_data).encode()
            
            for neighbor, (ip, _) in self.vizinhos_manager.VIZINHOS.items():
                if neighbor not in self.vizinhos_manager.vizinhos_inativos:
                    self.udp_socket.sendto(encoded_message, (ip, LSA_PORT))
                    
            stop_event.wait(0.5)

    def receber_lsa(self, lsa_database: Dict[str, Any], stop_event: Event) -> None:
        """
        Receive and process Link State Advertisements.
        
        Listens for incoming LSAs, updates the database, and forwards to other neighbors.
        
        Args:
            lsa_database: Database storing LSA information
            stop_event: Threading event to control the receiving loop
        """
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver_socket.bind(("0.0.0.0", LSA_PORT))
        
        while not stop_event.is_set():
            try:
                data, address = receiver_socket.recvfrom(4096)
                sender_ip = address[0]
                lsa_message = json.loads(data.decode())
                source_router = lsa_message["id"]
                
                if (source_router not in lsa_database or 
                    lsa_message["seq"] > lsa_database[source_router]["seq"]):
                    lsa_database[source_router] = lsa_message
                    
                    # Forward LSA to other neighbors
                    for neighbor, (ip, _) in self.vizinhos_manager.VIZINHOS.items():
                        if (ip != sender_ip and 
                            neighbor not in self.vizinhos_manager.vizinhos_inativos):
                            receiver_socket.sendto(data, (ip, LSA_PORT))
                            print(f"[{self.ROTEADOR_ID}] Encaminhando LSA para {neighbor} ({ip})")
                            
            except socket.timeout:
                continue
