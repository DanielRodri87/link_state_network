all:
	@docker-compose up --build
	
gerar_compose:
	@cd gera_yml && pip install --quiet -r requirements.txt
	@cd gera_yml && python3 gerar_yaml.py
	@cd gera_yml && python3 docker_compose_create.py

down:
	@docker-compose down 
	
clean:
	docker compose down --rmi all --volumes --remove-orphans

teste_ping:
	@cd docker/roteador/test && python3 teste_ping.py

teste_rotas:
	@cd docker/roteador/test && python3 teste_rotas.py

teste_vias:
	@cd docker/roteador/test && python3 teste_vias.py

teste_ping_host:
	@cd docker/host/script_teste && python3 teste_ping.py

install_deps:
	pip install --break-system-packages networkx matplotlib pyyaml

topologia:
	@cd docker/roteador/test && python3 mostrar_topologia.py