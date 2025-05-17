"""
Network Path Testing Module

This module provides functionality for testing and displaying network routes
and paths between routers in a Docker network environment.
"""

import subprocess
import sys
import os
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from class_net.manipulation import Manipulacao
from class_net.message import Mensagem

def teste_de_vias() -> None:
    """
    Test and display IP routes for all routers.
    
    Executes 'ip route' command on each router and displays the routing information.
    """
    router_list = Manipulacao.roteadores_encontrados()
    print(router_list)
    
    for source_router in router_list:
        print(f"Testando {source_router}...")
        try:
            route_command = f"docker exec {source_router} ip route"
            command_result = subprocess.run(
                route_command, 
                shell=True, 
                check=True, 
                text=True, 
                capture_output=True
            )
            if command_result.returncode == 0:
                print(
                    Mensagem.formatar_mensagem(source_router, (255, 255, 0)), 
                    ':', 
                    Mensagem.formatar_sucesso(command_result.stdout)
                )
                route_count = len(Manipulacao.extrair_linhas(command_result.stdout))
                print("Quantidade de linhas:", route_count)
                
        except subprocess.CalledProcessError:
            print(Mensagem.formatar_erro(f"{source_router} falhou."))
            
def teste_de_vias_table() -> None:
    """
    Test and display routing tables for all routers.
    
    Executes 'route -n' command on each router and displays the routing table.
    """
    router_list = Manipulacao.roteadores_encontrados()
    print(router_list)
    
    for source_router in router_list:
        print(f"Testando {source_router}...")
        try:
            route_command = f"docker exec {source_router} route -n"
            command_result = subprocess.run(
                route_command, 
                shell=True, 
                check=True, 
                text=True, 
                capture_output=True
            )
            if command_result.returncode == 0:
                print(
                    Mensagem.formatar_mensagem(source_router, (255, 255, 0)), 
                    ':', 
                    Mensagem.formatar_sucesso(command_result.stdout)
                )
                route_count = len(Manipulacao.extrair_linhas(command_result.stdout))
                print("Quantidade de linhas:", route_count)
                
        except subprocess.CalledProcessError:
            print(Mensagem.formatar_erro(f"{source_router} falhou."))

def teste() -> None:
    """Test traceroute functionality between specific routers."""
    try:
        trace_command = "docker exec roteador2 traceroute 172.21.7.1"
        command_result = subprocess.run(
            trace_command, 
            shell=True, 
            check=True, 
            text=True, 
            capture_output=True
        )
        if command_result.returncode == 0:
            path = Manipulacao.traduzir_caminho('roteador2', command_result.stdout)
            print(path)
    except subprocess.CalledProcessError:
        print(Mensagem.formatar_erro("roteador2 -> 172.21.7.1 falhou."))

if __name__ == "__main__":
    teste_de_vias()
    teste_de_vias_table()
    print("Teste de vias concluído.")