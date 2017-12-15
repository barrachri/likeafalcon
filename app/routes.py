from app.views import websocket, index
from app.api import handle, query_db

routes = (
    ('POST', '/v1/json', handle),
    ('GET', '/query', query_db),
    ('GET', '/ws', websocket),
    ('GET', '/', index),
)
