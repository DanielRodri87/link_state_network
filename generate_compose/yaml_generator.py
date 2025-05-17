"""
YAML Configuration Generator Module

This module generates network topology configurations in YAML format for Docker networks.
It supports various network topologies including ring, star, fully connected, tree, and line.
"""

import os
import random
import yaml
import ipaddress
from typing import Dict, List, Any, Union

def gerar_yaml(num_roteadores: int, hosts_por_rede: int, topologia: str = "estrela") -> None:
    """
    Generate YAML configuration for a network topology.

    Args:
        num_roteadores: Number of routers in the network
        hosts_por_rede: Number of hosts per network segment
        topologia: Network topology type ("anel", "estrela", "totalmente_conectada", "tree", "linha")

    Raises:
        ValueError: If invalid parameters are provided
    """
    if num_roteadores < 3:
        raise ValueError("Número de roteadores deve ser pelo menos 3.")
    if hosts_por_rede < 1 or hosts_por_rede > 254:
        raise ValueError("Número de hosts por rede deve ser entre 1 e 254.")

    redes = []
    roteadores = []
    hosts = []

    base_ip = ipaddress.IPv4Network("172.21.0.0/16")
    subnets = list(base_ip.subnets(new_prefix=24))

    for i in range(num_roteadores):
        rede_nome = f"rede{i+1}"
        subnet = subnets[i]
        gateway = subnet.network_address + 1

        redes.append({
            'name': rede_nome,
            'subnet': str(subnet),
            'gateway': str(gateway)
        })

        for j in range(hosts_por_rede):
            ip_host = subnet.network_address + 10 + j
            router_ip = subnet.network_address + 2

            hosts.append({
                'name': f'host{i+1}{chr(97+j)}',
                'network': rede_nome,
                'router': str(router_ip),
                'ip': str(ip_host)
            })

    for i in range(num_roteadores):
        id_roteador = f"roteador{i+1}"
        network_config = setup_network_topology(i, {'networks': redes}, num_roteadores, topologia)
        roteadores.append({
            'id': id_roteador,
            'ip': str(network_config['networks'][0]['ip']),
            'networks': network_config['networks'],
            'neighbors': network_config['neighbors']
        })

    dados = {
        'networks': redes,
        'routers': roteadores,
        'hosts': hosts
    }

    # Update config file path handling
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(config_dir, 'config.yaml')
    
    # Ensure directory exists
    os.makedirs(config_dir, exist_ok=True)
    
    with open(config_path, 'w') as file:
        yaml.dump(dados, file, sort_keys=False, default_flow_style=False)

    print(f"\n✅ Arquivo '{config_path}' gerado com sucesso para topologia '{topologia}'!\n")

def setup_network_topology(router_index: int, network_config: Dict[str, Any], 
                         num_routers: int, topology: str) -> Dict[str, Any]:
    """
    Configure network topology for a specific router.

    Args:
        router_index: Index of the current router
        network_config: Current network configuration
        num_routers: Total number of routers
        topology: Type of network topology

    Returns:
        Dict containing networks and neighbors configuration
    """
    networks = []
    neighbors = []
    
    # Host network configuration
    host_network = network_config['networks'][router_index]
    host_ip = ipaddress.IPv4Address(host_network['gateway']) + 1
    networks.append({'name': host_network['name'], 'ip': str(host_ip)})

    if topology == "anel":
        # Ring topology configuration
        adjacent_networks = [network_config['networks'][(router_index + offset) % num_routers] 
                           for offset in [1, -1]]
        
        prev_ip = ipaddress.IPv4Address(adjacent_networks[1]['gateway']) + 3
        next_ip = ipaddress.IPv4Address(adjacent_networks[0]['gateway']) + 2
        
        networks.extend([
            {'name': adjacent_networks[0]['name'], 'ip': str(next_ip)},
            {'name': adjacent_networks[1]['name'], 'ip': str(prev_ip)}
        ])
        
        neighbors = [
            {'id': f'roteador{((router_index - 1) % num_routers) + 1}', 'cost': 10},
            {'id': f'roteador{((router_index + 1) % num_routers) + 1}', 'cost': 10}
        ]
    
    elif topology == "estrela":
        # Star topology configuration
        if router_index == 0:
            for j in range(1, num_routers):
                neighbor_network = network_config['networks'][j]
                neighbor_ip = ipaddress.IPv4Address(neighbor_network['gateway']) + 2
                networks.append({'name': neighbor_network['name'], 'ip': str(neighbor_ip)})
                neighbors.append({'id': f'roteador{j+1}', 'cost': 10})
        else:
            central_ip = ipaddress.IPv4Address(network_config['networks'][0]['gateway']) + 3 + (router_index - 1)
            networks.append({'name': network_config['networks'][0]['name'], 'ip': str(central_ip)})
            neighbors.append({'id': 'roteador1', 'cost': 10})

    elif topology == "tree":
        # Tree topology configuration
        left = 2 * router_index + 1
        right = 2 * router_index + 2

        if left < num_routers:
            neighbor_network = network_config['networks'][left]
            neighbor_ip = ipaddress.IPv4Address(neighbor_network['gateway']) + 2
            networks.append({'name': neighbor_network['name'], 'ip': str(neighbor_ip)})
            neighbors.append({'id': f'roteador{left+1}', 'cost': 10})

        if right < num_routers:
            neighbor_network = network_config['networks'][right]
            neighbor_ip = ipaddress.IPv4Address(neighbor_network['gateway']) + 2
            networks.append({'name': neighbor_network['name'], 'ip': str(neighbor_ip)})
            neighbors.append({'id': f'roteador{right+1}', 'cost': 10})

        if router_index != 0:
            parent = (router_index - 1) // 2
            parent_network = network_config['networks'][parent]
            parent_ip = ipaddress.IPv4Address(parent_network['gateway']) + 3 + (router_index - (2 * parent + 1))
            networks.append({'name': parent_network['name'], 'ip': str(parent_ip)})
            neighbors.append({'id': f'roteador{parent+1}', 'cost': 10})

    elif topology == "linha":
        # Line topology configuration
        if router_index < num_routers - 1:
            next_network = network_config['networks'][router_index + 1]
            next_ip = ipaddress.IPv4Address(next_network['gateway']) + 2
            networks.append({'name': next_network['name'], 'ip': str(next_ip)})
            neighbors.append({'id': f'roteador{router_index+2}', 'cost': 10})

        if router_index > 0:
            prev_network = network_config['networks'][router_index - 1]
            prev_ip = ipaddress.IPv4Address(prev_network['gateway']) + 3
            networks.append({'name': prev_network['name'], 'ip': str(prev_ip)})
            neighbors.append({'id': f'roteador{router_index}', 'cost': 10})
    else:
        raise ValueError(f"Topologia '{topology}' não suportada.")

    return {
        'networks': networks,
        'neighbors': neighbors
    }

def exibir_menu_topologias() -> str:
    """
    Display and handle the topology selection menu.

    Returns:
        str: Selected topology type
    """
    topology_options = {
        "1": "anel",
        "2": "estrela",
        "3": "tree",
        "4": "linha"
    }

    os.system('clear')
    print("╔════════════════════════════════════════════╗")
    print("║         🌐 GERADOR DE TOPOLOGIAS           ║")
    print("╠════════════════════════════════════════════╣")
    print("║ Escolha uma topologia para gerar:          ║")
    print("║                                            ║")
    print("║  1 - 🔄 Anel                               ║")
    print("║  2 - ⭐ Estrela                            ║")
    print("║  3 - 🌲 Tree (Árvore)                      ║")
    print("║  4 - 📏 Linha                              ║")
    print("╚════════════════════════════════════════════╝")

    while True:
        selected_option = input("\nDigite o número da topologia desejada: ").strip()
        if selected_option in topology_options:
            return topology_options[selected_option]
        print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    selected_topology = exibir_menu_topologias()
    input("\nPressione ENTER para continuar ou CTRL+C para cancelar...")
    gerar_yaml(6, 2, topologia=selected_topology)
