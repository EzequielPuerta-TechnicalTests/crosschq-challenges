run:
	make migrate
	pipenv run python manage.py runserver

migrate:
	pipenv run python manage.py migrate

migrations:
	pipenv run python manage.py makemigrations

coverage:
	@pipenv run coverage html
	@echo
	@echo "Generating coverage report..."
	@printf '**** Code Coverage Total: \033[30;48;5;82m  '
	@echo -n $(shell pipenv run coverage report | grep TOTAL | awk '{print $$4}')
	@printf '  \033[0m **** '
	@echo

shell:
	pipenv run python manage.py shell

import_books:
	pipenv run python manage.py import_books

test:
	pipenv run pytest -s --durations=10 --create-db
