.PHONY: help
.ONESHELL:
SHELL = /bin/bash

help: ## Print help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_.-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help
init: down volume up ## Init Project
down: ## Stop all compose services
	docker compose down --remove-orphans
volume: ## Remove all containers volumes
	docker volume prune -f
pull: ## Pull images
	docker compose pull
build: ## Build Docker services
	docker compose build --no-cache
up: pull build ## Run all services
	docker compose up -d
	make drop-db
	make migrate
	make ps
ps: ## Show all services
	docker compose ps
prune: ## Remove all volumes, containers and services
	make down
	make volume
	docker system prune -f
migrations: ## Make migrations
	docker exec -it psychology_web python3 manage.py makemigrations
migrate: migrations ## Run migrate
	docker exec -it psychology_web python3 manage.py migrate
shell: shell ## Run migrate
	docker exec -it psychology_web python3 manage.py shell
superuser: ## Create django superuser
	docker exec -it psychology_web python3 manage.py createsuperuser
dumpdata: ## regenerate fixture over all models
	docker exec -it psychology_web python3 manage.py dump_limited_data
bulk-loaddata: ## regenerate fixture over all models
	docker exec -it psychology_web python3 manage.py loaddata tests/fixtures/json/AuthUser.json tests/fixtures/json/*.json
clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -delete
lint: ## Run linters
	docker compose run --rm -v /app/ web sh -c "black apps/ && isort apps/ --profile black && flake8 apps/ && safety check"
lint-tests:
	docker compose run --rm -v /app/ web sh -c "black tests/ && isort tests/ --profile black"
pyenv-python: ## Install python
	pyenv install -s 3.11
pyenv-create-env:
	pyenv virtualenv -f 3.11 psychology_env
pyenv-init-env:
	pyenv shell psychology_env
	pip install poetry
	poetry config virtualenvs.create false
	poetry install --no-root --without dev
pyenv-env: ## Active python env
	pyenv shell psychology_env
pyenv-install: ## Install python dependencies
	poetry config virtualenvs.create false
	poetry install --no-root --without dev
pyenv-init: pyenv-python pyenv-create-env pyenv-env ## Initialize python env
drop-db: ## drop all tables in database
	docker exec -it psychology_postgres psql -U postgres -d psychology_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
collectstatic:
	docker exec -it psychology_web python3 manage.py collectstatic --noinput
