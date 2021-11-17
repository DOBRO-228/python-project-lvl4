install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	pip install --user ~/Desktop/hexlet_projects/python-project-lvl4/dist/*.whl
package-reinstall:
	pip install --user ~/Desktop/hexlet_projects/python-project-lvl4/dist/*.whl --force-reinstall
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml
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
export_req:
	poetry export -f requirements.txt --output requirements.txt