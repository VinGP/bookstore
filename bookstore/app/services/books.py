from app.models.authors import Author
from app.models.books import Book
from app.models.categories import Category
from app.models.images import Image
from app.models.publishers import Publisher
from app.models.series import Series


def create_book(
    session,
    title: str,
    isbn: str,
    annotation: str,
    price: int,
    publisher: Publisher,
    authors: list[Author],
    year: int,
    number_of_pages: int,
    available_quantity: int = 0,
    other_images: list[Image] = None,
    categories: list[Category] = None,
    size: str = "0 x 0 x 0",
    weight: int = 0,
    image_path: str = None,
    series: list[Series] = None,
):
    book = session.query(Book).filter_by(isbn=isbn).one_or_none()
    if book:
        return book

    book = Book()
    book.isbn = isbn
    book.title = title
    book.annotation = annotation
    book.price = price
    book.publisher = publisher
    for author in authors:
        book.authors.append(author)
    book.year = year
    book.number_of_pages = number_of_pages
    book.available_quantity = available_quantity
    if other_images:
        for img in other_images:
            book.other_images.append(img)
    if categories:
        for category in categories:
            book.categories.append(category)
    book.size = size
    book.weight = weight
    if series:
        for s in series:
            book.series.append(s)
    if image_path:
        book.image_path = image_path
    session.add(book)
    session.commit()
    return book
