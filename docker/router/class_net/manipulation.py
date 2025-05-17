"""
Network Address Manipulation Module

This module provides utilities for manipulating and extracting network addresses
and router information in a Docker network environment.
"""

import subprocess
import re
from typing import List

class Manipulacao:
    """
    A class for manipulating network addresses and router configurations.
    
    Provides static methods for finding routers, extracting network information,
    and translating network paths.
    """
    
    @staticmethod
    def roteadores_encontrados() -> List[str]:
        """
        Find all router containers in the Docker environment.
        
        Returns:
            List[str]: List of router container names
        """
        docker_command = "docker ps --filter name=roteador --format '{{.Names}}'"
        command_result = subprocess.run(docker_command, shell=True, check=True, text=True, capture_output=True)
        router_list = [router.strip("'") for router in command_result.stdout.split('\n') if router]
        return router_list

    @staticmethod
    def extrair_numero_roteador(router_name: str) -> str:
        """
        Extract network address segment from router name.
        
        Args:
            router_name: Name of the router container
            
        Returns:
            str: Network address segment
        """
        return f"172.21.{int(router_name.split('roteador')[-1]) - 1}"

    @staticmethod
    def extrair_numero_roteador_ip(router_ip: str) -> str:
        """
        Extract network segment from router IP.
        
        Args:
            router_ip: IP address of the router
            
        Returns:
            str: Network segment
        """
        ip_segments = router_ip.split('.')[:-1]
        return '.'.join(ip_segments)

    @staticmethod
    def extrair_subnet_roteador_ip(router_ip: str) -> str:
        """
        Generate subnet address from router IP.
        
        Args:
            router_ip: IP address of the router
            
        Returns:
            str: Subnet address in CIDR notation
        """
        return f"{Manipulacao.extrair_numero_roteador_ip(router_ip)}.0/24"

    @staticmethod
    def extrair_ip_roteadores_ip(router_ip: str) -> str:
        """
        Generate router interface IP from router IP.
        
        Args:
            router_ip: Base IP address of the router
            
        Returns:
            str: Router interface IP address
        """
        return f"{Manipulacao.extrair_numero_roteador_ip(router_ip)}.2"

    @staticmethod
    def extrair_subnet_roteador(router_name: str) -> str:
        """
        Generate subnet address from router name.
        
        Args:
            router_name: Name of the router container
            
        Returns:
            str: Subnet address in CIDR notation
        """
        return f"{Manipulacao.extrair_numero_roteador(router_name)}.0/24"

    @staticmethod
    def extrair_ip_roteadores(router_name: str) -> str:
        """
        Generate router interface IP from router name.
        
        Args:
            router_name: Name of the router container
            
        Returns:
            str: Router interface IP address
        """
        return f"{Manipulacao.extrair_numero_roteador(router_name)}.2"

    @staticmethod
    def extrair_ip_gateway(router_name: str) -> str:
        """
        Generate gateway IP address from router name.
        
        Args:
            router_name: Name of the router container
            
        Returns:
            str: Gateway IP address
        """
        return f"{Manipulacao.extrair_numero_roteador(router_name)}.1"

    @staticmethod
    def extrair_linhas(result: str) -> List[str]:
        """
        Split result string into lines.
        
        Args:
            result: String to be split
            
        Returns:
            List[str]: List of lines
        """
        return result.split('\n')

    @staticmethod
    def traduzir_caminho(router: str, path: str, total_routers: int = 0) -> str:
        """
        Translate network path into human-readable format.
        
        Args:
            router: Source router name
            path: Raw path information
            total_routers: Total number of routers in network
            
        Returns:
            str: Formatted path string with router hops
        """
        hop_list = Manipulacao.extrair_linhas(path)
        translated_path = [router]

        for hop in hop_list[1:]:
            if 'roteador' in hop:
                router_name = hop.split()[1].split('.')[0]
                translated_path.append(router_name)
            elif hop and '(' in hop and ')' in hop:
                try:
                    n1, n2 = hop.split('(')[1].split(')')[0].split('.')[2:]
                    router_number = 0
                    
                    if n2 == '4':
                        router_number = int(n1) + 2
                        if router_number > total_routers:
                            router_number = router_number % total_routers
                    elif n2 == '3':
                        router_number = int(n1)
                        if router_number > total_routers:
                            router_number = router_number % total_routers
                    else:
                        router_number = int(n1) + 1
                    
                    translated_path.append(f'roteador{router_number}')
                except (ValueError, IndexError):
                    continue

        return ' -> '.join(translated_path)

if __name__ == "__main__":
    test_ip = '172.21.1.2'
    print(Manipulacao.extrair_numero_roteador_ip(test_ip))
    print(Manipulacao.extrair_subnet_roteador_ip(test_ip))
    print(Manipulacao.extrair_ip_roteadores_ip(test_ip))