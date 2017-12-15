"""APIs handlers."""

from json import JSONDecodeError

from aiohttp import web
from rampante import streaming
from sqlalchemy import select

from app.models import Event
from app.serializers import EventSchema


async def handle(request):
    try:
        data = await request.json()
    except JSONDecodeError:
        body = {"message": "Error inside your format message."}
        return web.json_response(body, status=400)
    if not data:
        return web.json_response({"message": "Empty json."}, status=400)

    await streaming.publish("like.a.falcon", data)
    # send data to active websockets
    for ws in request.app['websockets']:
        await ws.send_json(data)
    return web.json_response({"message": "We got your message."})


async def query_db(request):
    try:
        limit = int(request.query.get("limit", 10))
        offset = int(request.query.get("offset", 0))
    except ValueError:
        body = {"message": "Error inside you query params."}
        return web.json_response(body, status=400)

    query = select([Event]).limit(limit).offset(offset)
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(query)
        data = await result.fetchall()

    schema, _ = EventSchema(many=True).dump(data)
    body = {
        "events": schema,
        "limit": limit,
        "offset": offset
    }
    return web.json_response(body)
