from flask.cli import FlaskGroup

from app import app

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    pass


if __name__ == "__main__":
    cli()

# Создание копии базы данных из которой можно будет создать базу:
# pg_dump -U hello_flask -p 54320 -d hello_flask_dev  -f ./d.sql
# Запуск: python manage.py --env-file .env.dev run -h 0.0.0.0
