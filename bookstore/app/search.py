from app import app
from flask import current_app


def add_to_index(index, model):
    with app.app_context():
        if not current_app.elasticsearch:
            return
        payload = model.get_payload()
        current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0

    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "authors^2", "*"],
                # "fuzziness": "AUTO",
                "fuzziness": 2,
                # "operator": "and",
                "boost": 1.0,
                "type": "best_fields",
                # "type": "most_fields",
                # "prefix_length": 2
            },
        },
        "from": (page - 1) * per_page,
        "size": per_page,
    }

    search = current_app.elasticsearch.search(index=index, body=body)

    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    hits = search["hits"]["hits"]
    return ids, search["hits"]["total"]["value"], hits
