from app.search import add_to_index, query_index
from sqlalchemy import case


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total, hits = query_index(cls.__tablename__, expression, page, per_page)
        print(ids, total)
        if total == 0:
            return [], 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        from app.models.db_session import create_session

        with create_session() as db_sess:
            return (
                db_sess.query(cls)
                .filter(cls.id.in_(ids))
                .order_by(case(*when, value=cls.id)),
                total,
            )

    @classmethod
    def autocomplete(cls, expression, page, per_page):
        ids, total, hits = query_index(cls.__tablename__, expression, page, per_page)
        return [i["_source"]["title"] for i in hits]

    # @classmethod
    # def before_commit(cls, session, *a, **kwargs):
    #     print("before_commit", session, *a, **kwargs)
    #
    #     session._changes = {
    #         'add': list(session.new),
    #         'update': list(session.dirty),
    #         'delete': list(session.deleted)
    #     }
    #
    # @classmethod
    # def after_commit(cls, session, *a, **kwargs):
    #     print("after_commit", session, *a, **kwargs)
    #     for obj in session._changes['add']:
    #         if isinstance(obj, SearchableMixin):
    #             add_to_index(obj.__tablename__, obj)
    #     for obj in session._changes['update']:
    #         if isinstance(obj, SearchableMixin):
    #             add_to_index(obj.__tablename__, obj)
    #     for obj in session._changes['delete']:
    #         if isinstance(obj, SearchableMixin):
    #             remove_from_index(obj.__tablename__, obj)
    #     session._changes = None

    @classmethod
    def reindex(cls):
        from app.models.db_session import create_session

        c = 0
        with create_session() as db_sess:
            for obj in db_sess.query(cls):
                c += 1
                print(c)
                add_to_index(cls.__tablename__, obj)
