from flask.cli import FlaskGroup

from app import app, db

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    # docker-compose exec web python manage.py create_db
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()

# Создание копии базы данных из которой можно будет создать базу:
# pg_dump -U hello_flask -p 54320 -d hello_flask_dev  -f ./d.sql
# Запуск: python manage.py --env-file .env.dev run -h 0.0.0.0
