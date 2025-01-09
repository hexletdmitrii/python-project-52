lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-coverage:
	coverage run manage.py test
	coverage report
	coverage xml

install:
	poetry install

selfcheck:
	poetry check

check: selfcheck test-coverage lint

dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

shell:
	poetry run python manage.py shell_plus --ipython
