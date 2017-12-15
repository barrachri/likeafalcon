from app.views import handle, query_db, websocket

routes = (
    ('POST', '/v1/json', handle),
    ('GET', '/query', query_db),
    ('GET', '/ws', websocket),
)
