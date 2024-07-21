server:
	poetry run python manage.py runserver
migrations:
	poetry run python manage.py makemigrations
migrate:
	poetry run python manage.py migrate
test:
	poetry run python manage.py test
