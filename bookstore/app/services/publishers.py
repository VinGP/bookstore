from app.models.db_session import create_session
from app.models.publishers import Publisher


def create_publisher(name: str, address: str = None, phone: str = None):
    with create_session() as db_sess:
        publisher = (
            db_sess.query(Publisher)
            .filter_by(name=name, address=address, phone=phone)
            .one_or_none()
        )
        if publisher:
            return publisher
    publisher = Publisher()
    publisher.name = name
    publisher.address = address
    publisher.phone = phone
    with create_session() as db_sess:
        db_sess.add(publisher)
        db_sess.commit()
        return publisher
