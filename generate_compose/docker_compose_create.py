"""
Docker Compose Generator Module

This module generates a docker-compose.yml file based on a configuration template.
It processes router configurations, network settings, and host configurations to create
a complete Docker network topology.
"""

import yaml
from jinja2 import Environment, FileSystemLoader
import os
from typing import Dict, List, Any

def process_router_neighbors(router: Dict[str, Any], all_routers: List[Dict[str, Any]]) -> List[str]:
    """
    Process neighbor information for a router and format connection strings.
    
    Args:
        router: Dictionary containing router configuration
        all_routers: List of all router configurations
        
    Returns:
        List of formatted neighbor connection strings
    """
    neighbor_connections = []
    for neighbor in router['neighbors']:
        neighbor_config = next(r for r in all_routers if r['id'] == neighbor['id'])
        neighbor_ip = neighbor_config['networks'][0]['ip']
        connection_str = f'"{neighbor["id"]}":["{neighbor_ip}",{neighbor["cost"]}]'
        neighbor_connections.append(connection_str)
    return neighbor_connections

def main() -> None:
    """
    Main function to generate docker-compose.yml from template and configuration.
    
    Reads configuration from config.yaml, processes router and network settings,
    and generates a docker-compose.yml file using Jinja2 templating.
    """
    template_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load configuration file
    config_path = os.path.join(template_dir, 'config.yaml')
    with open(config_path) as config_file:
        network_config = yaml.safe_load(config_file)

    # Process router configurations
    processed_routers = []
    for router_config in network_config['routers']:
        neighbor_strings = process_router_neighbors(router_config, network_config['routers'])
        processed_routers.append({
            **router_config,
            'neighbors_str': ','.join(neighbor_strings)
        })

    # Initialize Jinja2 environment
    template_env = Environment(loader=FileSystemLoader(template_dir))
    compose_template = template_env.get_template('docker-compose.j2')

    # Generate docker-compose.yml content
    compose_output = compose_template.render(
        routers=processed_routers,
        hosts=network_config['hosts'],
        networks=network_config['networks']
    )

    # Write output to file
    with open('docker-compose.yml', 'w') as compose_file:
        compose_file.write(compose_output)

    print("Arquivo docker-compose.yml gerado com sucesso.")

if __name__ == '__main__':
    main()
