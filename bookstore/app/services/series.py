from app.models.db_session import create_session
from app.models.publishers import Publisher
from app.models.series import Series


def create_series(session, name: str, publisher: Publisher):
    series = (
        session.query(Series).filter_by(name=name, publisher=publisher).one_or_none()
    )
    if series:
        return series
    series = Series()
    series.name = name
    series.publisher = publisher
    session.add(series)
    session.commit()
    return series


def get_series_by_id(session, id):
    series = session.query(Series).get(id)
    return series
