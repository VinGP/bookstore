import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(database_url):
    global __factory

    if __factory:
        return

    print(f"Подключение к базе данных по адресу {database_url}")

    engine = sa.create_engine(database_url, echo=True)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
