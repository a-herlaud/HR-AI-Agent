COMPOSE = docker compose \
	-f ./src/docker-compose.yml \
	--env-file .env

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down -v

exec-api:
	$(COMPOSE) exec -it kpi-api bash

exec-database:
	$(COMPOSE) exec -it database bash

up-test:
	docker build -t my-test-image ./test && \
		docker run --rm -it \
			--add-host=host.docker.internal:host-gateway \
			-v "./test/app:/app:Z" \
			my-test-image bash
		docker rmi my-test-image

fclean:
	$(COMPOSE) down -v --rmi local