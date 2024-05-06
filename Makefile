server:
	poetry run python manage.py runserver
makemig:
	python manage.py makemigrations
mig:
	python manage.py migrate