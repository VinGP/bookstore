up:
	docker compose up --build -d
create-db:
	docker compose  exec web python manage.py create_db
stop:
	docker compose stop
start:
	docker compose start
down:
	docker compose down
down-v:
	docker compose down -v