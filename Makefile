COMPOSE= docker compose -f src/docker-compose.yml

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down -v

exec-api:
	$(COMPOSE) exec -it kpi-api bash

up-test:
	docker build -t my-test-image ./test && \
	docker run --rm -it -v "./test/app:/app:Z" my-test-image bash

fclean:
	$(COMPOSE) down -v --rmi local