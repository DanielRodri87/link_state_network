import subprocess
import re

class Manipulacao:
    
    @staticmethod
    def roteadores_encontrados():
        comando = "docker ps --filter name=roteador --format '{{.Names}}'"
        result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
        roteadores = [r.strip("'") for r in result.stdout.split('\n') if r]
        return roteadores

    # destino_ip = Manipulacao.extrair_subnet_roteador_ip(destino)
    # prox_salto_ip = Manipulacao.extrair_ip_roteadores_ip(prox_salto)
    
    @staticmethod
    def extrair_numero_roteador(roteador_name):
        return f"172.21.{int(roteador_name.split('roteador')[-1]) - 1}"
    
    @staticmethod
    def extrair_numero_roteador_ip(ip_roteador):
        ip_ini = ip_roteador.split('.')[:-1]
        
        return '.'.join(ip_ini) 
    
    @staticmethod
    def extrair_subnet_roteador_ip(ip_roteador):
        return f"{Manipulacao.extrair_numero_roteador_ip(ip_roteador)}.0/24"
    
    @staticmethod
    def extrair_ip_roteadores_ip(ip_roteador):
        return f"{Manipulacao.extrair_numero_roteador_ip(ip_roteador)}.2"
    
    @staticmethod
    def extrair_subnet_roteador(roteador_name):
        return f"{Manipulacao.extrair_numero_roteador(roteador_name)}.0/24"
    
    @staticmethod
    def extrair_ip_roteadores(roteador_name):
        return f"{Manipulacao.extrair_numero_roteador(roteador_name)}.2"
    
    @staticmethod
    def extrair_ip_gateway(roteador_name):
        return f"{Manipulacao.extrair_numero_roteador(roteador_name)}.1"
    
    @staticmethod
    def extrair_linhas(resultado):
        linhas = resultado.split('\n')
        return linhas
    
    @staticmethod
    def traduzir_caminho(origem, traceroute_output):
        caminho = [origem]
        hops = traceroute_output.split('\n')
        ip_pattern = re.compile(r'\((.*?)\)')  # Regex to find IPs in parentheses
        
        for hop_line in hops[1:]:  # Skip the first line (header)
            if not hop_line.strip():
                continue
            # Find all IPs in the line
            ips = ip_pattern.findall(hop_line)
            if ips:
                # Take the first IP found
                ip = ips[0]
                octets = ip.split('.')
                if len(octets) >= 3:
                    try:
                        numero_roteador = int(octets[2]) + 1
                        caminho.append(f"roteador{numero_roteador}")
                    except (ValueError, IndexError):
                        # Handle invalid octet or index error
                        caminho.append("unknown")
            else:
                # No IP found (e.g., timeout '*')
                caminho.append("*")
        
        return ' -> '.join(caminho)

    
if __name__ == "__main__":
    # Teste da classe Manipulacao
    ip = '172.21.1.2'
    
    print(Manipulacao.extrair_numero_roteador_ip(ip))
    print(Manipulacao.extrair_subnet_roteador_ip(ip))
    print(Manipulacao.extrair_ip_roteadores_ip(ip))