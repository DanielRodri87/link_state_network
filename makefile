all:
	@docker-compose up --build

down:
	@docker-compose down 
	
clean:
	docker compose down --rmi all --volumes --remove-orphans

ping:
	@cd docker/router/test && python3 ping_test.py

rotas:
	@cd docker/router/test && python3 route_test.py

vias:
	@cd docker/router/test && python3 path_test.py

ping_host:
	@cd docker/host/test_script && python3 ping_test.py

topologia:
	@cd docker/router/test && python3 show_topology.py

limiar:
	@cd docker/router/test && python3 thresholds.py

install_deps:
	pip install --break-system-packages networkx matplotlib pyyaml