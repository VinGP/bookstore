from app.models.authors import Author


def create_author(
    session, first_name: str, second_name: str = " ", surname: str = None, *a
):
    author = (
        session.query(Author)
        .filter_by(first_name=first_name, second_name=second_name, surname=surname)
        .one_or_none()
    )
    if author:
        return author
    author = Author()
    author.first_name = first_name
    author.second_name = second_name
    if surname:
        author.surname = surname
    session.add(author)
    session.commit()
    return author
