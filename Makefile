include ./tools/env/.env
export

default: run

run: start-backend start-frontend

start-backend:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -tf

build: purge docker-build collectstatic migrate build-frontend

build-frontend:
	cd frontend && npm install && cd ..

start-frontend:
	cd frontend && npm run start && cd ..

docker-build:
	docker-compose build

collectstatic:
	docker-compose run --rm cli python manage.py collectstatic --noinput

migrate:
	docker-compose run --rm cli python manage.py migrate ${app_name}

load-initial-fixtures:
	docker-compose run --rm cli python manage.py loaddata /app/fixtures/initial_data.json

export-fixtures:
	@docker-compose run --rm cli python manage.py dumpdata --format=json

makemigrations:
	docker-compose run --rm cli python manage.py makemigrations ${app_name}

flush-db:
	docker-compose run --rm cli python manage.py flush --noinput

reset-db:
	docker-compose run --rm cli python manage.py reset_db -c --noinput

createsuperuser:
	docker-compose run --rm cli python manage.py createsuperuser

export-dev-db:
	@docker-compose run --rm db pg_dump --dbname=${DATABASE_URL}

cli:
	docker-compose run --rm cli sh

purge:
	docker-compose down -v --remove-orphans
	rm -rf ./api/static/*

app:
	docker-compose run --rm cli python manage.py startapp ${app_name}

test:
	docker-compose run --rm cli python manage.py test