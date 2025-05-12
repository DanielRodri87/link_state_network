import yaml
from jinja2 import Environment, FileSystemLoader
import os 
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(script_dir, 'config.yaml')) as f:
        config = yaml.safe_load(f)

    routers = []
    for router in config['routers']:
        neighbors = []

        for neighbor in router['neighbors']:
            neighbor_router = next(r for r in config['routers'] if r['id'] == neighbor['id'])
            neighbor_ip = neighbor_router['networks'][0]['ip']
            neighbors.append(f'"{neighbor["id"]}":["{neighbor_ip}",{neighbor["cost"]}]')

        routers.append({
            **router,
            'neighbors_str': ','.join(neighbors)
        })

    # Configurar o ambiente Jinja2
    env = Environment(loader=FileSystemLoader(script_dir))
    template = env.get_template('docker-compose.j2')

    # Renderizar o template com os dados
    output = template.render(
        routers=routers,
        hosts=config['hosts'],
        networks=config['networks']
    )

    # Salvar o docker-compose.yml gerado
    with open('../docker-compose.yml', 'w') as f:
        f.write(output)

    print("Arquivo docker-compose.yml gerado com sucesso.")

if __name__ == '__main__':
    main()
