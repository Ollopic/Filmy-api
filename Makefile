help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: docs

init: ## init project
	@docker compose down -v
	@$(MAKE) start
	@$(MAKE) log

start: ## start containers
	@docker compose up -d --build

stop: ## stop containers
	@docker compose stop

restart: ## restart containers
	@docker compose restart

log: ## log api and db containers
	@docker compose logs -f --tail 100

log-api: ## log api container
	@docker compose logs -f --tail 100 api

log-db: ## log db container
	@docker compose logs -f --tail 100 db

lint: ## check errors in python code without fixing them
	@docker compose exec api ruff check ${DIR_TO_REFAC}
unsafe-fixes: ## fix python code for unsafe issues
	@docker compose exec api ruff check --fix --unsafe-fixes ${DIR_TO_REFAC}
format: ## format python code and sort import
	@docker compose exec api ruff format ${DIR_TO_REFAC}
	@docker compose exec api ruff check --select I --fix ${DIR_TO_REFAC}