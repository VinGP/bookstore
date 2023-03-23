from app.models.images import Image


def create_image(session, filename: str, book_id: int):
    image = Image()
    image.filename = "image/book/" + filename
    image.book_id = book_id
    session.add(image)
    session.commit()
    return image
