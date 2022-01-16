install:
	poetry install
lint:
	poetry run flake8 task_manager labels statuses tasks users mixins.py
test:
	poetry run python3 manage.py test
coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
test-coverage_mine:
	poetry run pytest --cov=page_loader
sort:
	poetry run isort .
start:
	poetry run python3 manage.py runserver
start_gunicorn:
	poetry run gunicorn task_manager.wsgi
start_app:
	poetry run python3 manage.py startapp authentication
shell:
	poetry run python3 manage.py shell
make_migrations:
	poetry run python3 manage.py makemigrations
migrate:
	poetry run python3 manage.py migrate
export_req:
	poetry export -f requirements.txt --output requirements.txt
make_fixture:
	poetry run python3 manage.py dumpdata labels.Label --pk 1 --indent 4 > fixtures/labels.json