local start:

```shell
docker-compose up --build -d
docker-compose exec web python manage.py create_db
```

или с помощью make

```shell
make dev create-db
```

Для разработки

```shell
git clone https://github.com/VinGP/bookstore.git
cd bookstore
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
```

Для развертывания на сервере

```shell
git clone https://github.com/VinGP/bookstore.git
cd bookstore
```

Создайте контейнеры вручную:

```shell
docker-compose -f docker-compose.prod.yml up --build -d
docker-compose exec web python manage.py create_db
```

или с помощью make:

```shell
make prod create-db
```

