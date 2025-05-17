"""
Network connectivity testing module for Docker containers.

This module provides functionality to test network connectivity between hosts
and routers in a Docker network environment using ICMP ping.
"""

import subprocess
from typing import List, Tuple
from host import Host

def teste_de_ping_hosts() -> None:
    """
    Test network connectivity between all host containers.
    
    Performs ICMP ping tests between all host containers in the network
    and reports success or failure for each connection attempt.
    """
    failed_connections: List[Tuple[str, str]] = []
    host_list = Host.host_encontrados()
    
    for source_host in host_list:
        print(f"Testando {source_host}...")
        for target_host in host_list:
            try:
                ping_command = (
                    f"docker exec {source_host} ping -c 1 -W 0.1 "
                    f"172.21.{Host.extrair_ip_hosts(target_host)}"
                )
                ping_result = subprocess.run(
                    ping_command, 
                    shell=True, 
                    check=True, 
                    text=True, 
                    capture_output=True
                )
                if ping_result.returncode == 0:
                    print(Host.formatar_sucesso(f"{source_host} -> {target_host} sucesso."))
            except subprocess.CalledProcessError:
                print(Host.formatar_erro(f"{source_host} -> {target_host} falhou."))
                failed_connections.append((source_host, target_host))
        print('\n')
    
    if failed_connections:
        print("Host com falha:")
        for source, target in failed_connections:
            print(Host.formatar_erro(f"{source} -> {target} falhou."))
        print('\n')

def teste_de_ping_roteadores() -> None:
    """
    Test network connectivity between hosts and routers.
    
    Performs ICMP ping tests from each host to all routers in the network
    and reports success or failure for each connection attempt.
    """
    failed_connections: List[Tuple[str, str]] = []
    router_list = Host.roteadores_encontrados()
    host_list = Host.host_encontrados()
    
    for source_host in host_list:
        print(f"Testando {source_host}...")
        for target_router in router_list:
            try:
                ping_command = (
                    f"docker exec {source_host} ping -c 1 "
                    f"172.21.{Host.extrair_ip_roteadores(target_router)}.2"
                )
                ping_result = subprocess.run(
                    ping_command, 
                    shell=True, 
                    check=True, 
                    text=True, 
                    capture_output=True
                )
                if ping_result.returncode == 0:
                    print(Host.formatar_sucesso(f"{source_host} -> {target_router} sucesso."))
            except subprocess.CalledProcessError:
                print(Host.formatar_erro(f"{source_host} -> {target_router} falhou."))
                failed_connections.append((source_host, target_router))
        print('\n')

    if failed_connections:
        print("Hosts com falha:")
        for source, target in failed_connections:
            print(Host.formatar_erro(f"{source} -> {target} falhou."))
        print('\n')

if __name__ == "__main__":
    teste_de_ping_hosts()
    print("Teste de ping concluído.")