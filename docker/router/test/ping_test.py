"""
Router Connectivity Testing Module

This module provides functionality to test and verify network connectivity
between routers in a Docker network environment using ICMP ping.
"""

import subprocess
import sys
import os
from typing import List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from class_net.manipulation import Manipulacao
from class_net.message import Mensagem

def teste_de_ping_roteadores() -> None:
    """
    Test network connectivity between all routers.
    
    Performs ICMP ping tests between all router pairs in the network
    and reports success or failure for each connection attempt.
    """
    failed_connections: List[Tuple[str, str]] = []
    router_list = Manipulacao.roteadores_encontrados()
    
    for source_router in router_list:
        print(f"Testando {source_router}...")
        for target_router in router_list:
            try:
                target_ip = Manipulacao.extrair_ip_roteadores(target_router)
                ping_command = f"docker exec {source_router} ping -c 1 -W 0.1 {target_ip}"
                command_result = subprocess.run(
                    ping_command, 
                    shell=True, 
                    check=True, 
                    text=True, 
                    capture_output=True
                )
                if command_result.returncode == 0:
                    print(Mensagem.formatar_sucesso(
                        f"{source_router} -> {target_router} sucesso."
                    ))
            except subprocess.CalledProcessError:
                print(Mensagem.formatar_erro(
                    f"{source_router} -> {target_router} falhou."
                ))
                failed_connections.append([source_router, target_router])
        print('\n')
        
    if failed_connections:
        print("Roteadores com falha:")
        for source, target in failed_connections:
            print(Mensagem.formatar_erro(f"{source} -> {target} falhou."))
        print('\n')

if __name__ == "__main__":
    teste_de_ping_roteadores()
    print("Teste de ping concluído.")