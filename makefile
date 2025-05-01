all:
	@cd gera_yml && python3 gerar_yaml.py
	@cd gera_yml && python3 docker_compose_create.py
	@docker-compose up --build
	# @docker-compose up -d --build --remove-orphans

down:
	@docker-compose down 
	

clean:
	docker compose down --rmi all --volumes --remove-orphans

teste_ping:
	@clear
	@cd docker/roteador/script_teste && python3 teste_ping.py

teste_rotas:
	@clear
	@cd docker/roteador/script_teste && python3 teste_rotas.py

teste_vias:
	@clear
	@cd docker/roteador/script_teste && python3 teste_vias.py

teste_ping_host:
	@clear
	@cd docker/host/script_teste && python3 teste_ping.py

