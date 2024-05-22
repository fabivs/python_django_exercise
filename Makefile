.PHONY: up halt deps deps-update shell run run-shell db-migrate db-flush format check-formatted test

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

run-shell:
	python manage.py shell -i ipython

db-migrate:
	python manage.py migrate

db-flush:
	python manage.py flush

format:
	python -m black .

check:
	python -m black --check .

test:
	./manage.py test
