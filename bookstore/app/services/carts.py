from app.models.books import Book
from app.models.cart import Cart, CartBook


def add_book_to_cart(
    session,
    book: Book,
    cart: Cart,
):
    cart_book = CartBook()
    cart_book.book_id = book.id
    cart_book.cart_id = cart.id

    session.add(cart_book)
    session.commit()


def delete_book_in_cart(
    session,
    book: Book,
    cart: Cart,
):
    cart_item = (
        session.query(CartBook)
        .filter(CartBook.cart_id == cart.id, CartBook.book_id == book.id)
        .first()
    )
    session.delete(cart_item)
    session.commit()


def update_count_book_in_cart(session, book: Book, cart: Cart, count: int):
    cart_item = (
        session.query(CartBook)
        .filter(CartBook.cart_id == cart.id, CartBook.book_id == book.id)
        .first()
    )
    cart_item.count = count
    session.commit()
    return cart_item


def get_cart_total_price(session, cart: Cart):
    total_cart_price = 0
    for cb in session.query(CartBook).filter(CartBook.cart_id == cart.id).all():
        total_cart_price += cb.count * cb.book.price
    return total_cart_price


def get_count_books_in_cart(session, cart: Cart):
    count = 0
    cart = (
        session.query(Cart)
        .filter(
            Cart.id == cart.id,
        )
        .first()
    )

    for cart_book in cart.books:
        count += cart_book.count
    return count


def get_cart_weight(session, cart: Cart):
    weight = 0
    cart = (
        session.query(Cart)
        .filter(
            Cart.id == cart.id,
        )
        .first()
    )

    for cart_book in cart.books:
        weight += cart_book.book.weight * cart_book.count
    return weight
