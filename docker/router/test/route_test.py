"""
Router Path Testing Module

This module provides functionality for testing and verifying routing paths
between routers in a Docker network environment using traceroute.
"""

import subprocess
import sys
import os
from typing import List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from class_net.manipulation import Manipulacao
from class_net.message import Mensagem

def teste_de_rotas() -> None:
    """
    Test routing paths between all routers in the network.
    
    Executes traceroute between all router pairs and displays the path
    information using color-coded output.
    """
    failed_routes: List[Tuple[str, str]] = []
    router_list = Manipulacao.roteadores_encontrados()
    
    for source_router in router_list:
        print(f"Testando {source_router}...")
        for target_router in router_list:
            if source_router != target_router:
                try:
                    target_gateway = Manipulacao.extrair_ip_gateway(target_router)
                    trace_command = f"docker exec {source_router} traceroute {target_gateway}"
                    command_result = subprocess.run(
                        trace_command, 
                        shell=True, 
                        check=True, 
                        text=True, 
                        capture_output=True
                    )
                    if command_result.returncode == 0:
                        path = Manipulacao.traduzir_caminho(
                            source_router,
                            command_result.stdout,
                            len(router_list)
                        )
                        print(
                            Mensagem.formatar_mensagem(target_router, (255, 255, 0)),
                            ':',
                            Mensagem.formatar_sucesso(path)
                        )
                except subprocess.CalledProcessError:
                    print(Mensagem.formatar_erro(
                        f"{source_router} -> {target_router} falhou."
                    ))
                    failed_routes.append([source_router, target_router])
                    
    if failed_routes:
        print("Roteadores com falha:")
        for source, target in failed_routes:
            print(Mensagem.formatar_erro(f"{source} -> {target} falhou."))
        print('\n')

def teste() -> None:
    """Test a specific routing path for debugging purposes."""
    try:
        trace_command = "docker exec roteador5 traceroute 172.21.0.1"
        command_result = subprocess.run(
            trace_command, 
            shell=True, 
            check=True, 
            text=True, 
            capture_output=True
        )
        if command_result.returncode == 0:
            router_count = len(Manipulacao.roteadores_encontrados())
            path = Manipulacao.traduzir_caminho(
                'roteador5',
                command_result.stdout,
                router_count
            )
            print(Mensagem.formatar_sucesso(path))
    except subprocess.CalledProcessError:
        print(Mensagem.formatar_erro("roteador2 -> 172.21.7.1 falhou."))

if __name__ == "__main__":
    teste_de_rotas()
    print("Teste de rotas concluído.")