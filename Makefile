.PHONY: up halt deps deps-update shell run migrate format check-formatted

up:
	docker-compose up -d

halt:
	docker-compose down

deps:
	poetry install

deps-update:
	poetry update

shell:
	poetry shell

run:
	python manage.py runserver

migrate:
	python manage.py migrate

format:
	python -m black .

check:
	python -m black --check .
