from app.models.categories import Category


def create_category(session, name: str):
    category = session.query(Category).filter_by(name=name).one_or_none()
    if category:
        return category
    category = Category()
    category.name = name
    session.add(category)
    session.commit()
    return category


def add_sub_category(session, category: Category, subcategory: Category):
    if category == subcategory.parent:
        return
    category.children.append(subcategory)
    subcategory.parent = category
    session.commit()


def get_main_categorise(session):
    categories = session.query(Category).filter(Category.parent == None).all()  # noqa
    return categories
