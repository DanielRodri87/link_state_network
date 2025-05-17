import subprocess
from typing import List, Tuple

class Host:
    """
    A class to manage host and router operations in a Docker network environment.
    
    This class provides static methods for formatting messages, finding network entities,
    extracting IP addresses, and handling network paths.
    """
    
    def __init__(self):
        """Initialize a Host instance."""
        pass
    
    @staticmethod
    def formatar_mensagem(message: str, rgb_color: Tuple[int, int, int]) -> str:
        """
        Format a message with RGB color coding.
        
        Args:
            message (str): The message to be formatted
            rgb_color (tuple): RGB color values as (red, green, blue)
            
        Returns:
            str: ANSI color-formatted message
        """
        red, green, blue = rgb_color
        return f"\033[38;2;{red};{green};{blue}m{message}\033[0m"
    
    @staticmethod
    def formatar_sucesso(message: str) -> str:
        """
        Format a success message in green color.
        
        Args:
            message (str): The success message
            
        Returns:
            str: Green-colored formatted message
        """
        return Host.formatar_mensagem(message, (0, 255, 0))
    
    @staticmethod
    def formatar_erro(message: str) -> str:
        """
        Format an error message in red color.
        
        Args:
            message (str): The error message
            
        Returns:
            str: Red-colored formatted message
        """
        return Host.formatar_mensagem(message, (255, 0, 0))
    
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
    def extrair_ip_roteadores(router_name: str) -> int:
        """
        Extract IP address identifier from router name.
        
        Args:
            router_name (str): Name of the router container
            
        Returns:
            int: IP identifier for the router
        """
        return int(router_name.split('roteador')[-1]) - 1
    
    @staticmethod
    def extrair_linhas(result: str) -> List[str]:
        """
        Split result string into lines.
        
        Args:
            result (str): String to be split
            
        Returns:
            List[str]: List of lines from the input string
        """
        return result.split('\n')
    
    @staticmethod
    def traduzir_caminho(router: str, path: str) -> str:
        """
        Translate network path into human-readable format.
        
        Args:
            router (str): Source router name
            path (str): Raw path information
            
        Returns:
            str: Formatted path string with router hops
        """
        hop_list = Host.extrair_linhas(path)
        translated_path = []
        translated_path.append(router)
        
        for hop in hop_list:
            if 'roteador' in hop:
                router_name = hop.split()[1].split('.')[0]
                translated_path.append(router_name)
            elif hop:
                router_number = int(hop.split('(')[1].split(')')[0].split('.')[2]) + 1
                translated_path.append(f'roteador{router_number}')
                
        return ' -> '.join(translated_path)
    
    @staticmethod
    def host_encontrados() -> List[str]:
        """
        Find all host containers in the Docker environment.
        
        Returns:
            List[str]: List of host container names
        """
        docker_command = "docker ps --filter name=host --format '{{.Names}}'"
        command_result = subprocess.run(docker_command, shell=True, check=True, text=True, capture_output=True)
        host_list = [host.strip("'") for host in command_result.stdout.split('\n') if host]
        return host_list
    
    @staticmethod
    def extrair_ip_hosts(host_name: str) -> str:
        """
        Generate IP address for a host based on its container name.
        
        Args:
            host_name (str): Name of the host container
            
        Returns:
            str: Generated IP address for the host
        """
        base_ip = int(''.join(filter(str.isdigit, host_name.split('host')[-1][:-1])))
        suffix_char = host_name[-1].lower()
        offset = ord(suffix_char) - ord('a')
        return f"{base_ip - 1}.{10 + offset}"