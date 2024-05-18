.PHONY: up halt deps deps-update shell run migrate

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
