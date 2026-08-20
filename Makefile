COMPOSE = docker compose \
	-f ./src/docker-compose.yml \
	--env-file .env

up:
	$(COMPOSE) --profile app up --build -d

down:
	$(COMPOSE) --profile "*" down

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

ci-test: up
	$(COMPOSE) --profile test up --exit-code-from ci-test --abort-on-container-exit --no-deps ci-test


clean:
	$(COMPOSE) --profile "*" down --rmi local

fclean:
	$(COMPOSE) --profile "*" down -v --rmi local
