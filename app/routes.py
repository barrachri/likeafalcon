"""app routes."""

from app.api import handle, query_db
from app.views import index, websocket

routes = (
    ('POST', '/v1/json', handle),
    ('GET', '/query', query_db),
    ('GET', '/ws', websocket),
    ('GET', '/', index),
)
