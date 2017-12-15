from app.views import handle, query_db

routes = (
    ('POST', '/v1/json', handle),
    ('GET', '/query', query_db),
)
