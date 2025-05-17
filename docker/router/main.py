"""
Router Application Entry Point

This module serves as the main entry point for the router application.
It initializes and starts the router instance with its network operations.
"""

import os
from class_net.router import RoteadorApp

if __name__ == "__main__":
    router_instance = RoteadorApp()
    router_id = os.getenv('ROTEADOR_ID')
    print(f"[{router_id}] Iniciado...")
    router_instance.iniciar_threads()