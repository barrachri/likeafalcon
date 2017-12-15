from aiohttp import web
from json.decoder import JSONDecodeError
from rampante import streaming
from app.models import Event
from sqlalchemy import select
from app.serializers import EventSchema


async def handle(request):
    try:
        data = await request.json()
    except JSONDecodeError:
        return web.json_response(
            {"message": "Error inside your format message."}, status=400
            )
    if not data:
        return web.json_response({"message": "Empty json."}, status=400)

    await streaming.publish("like.a.falcon", data)

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


async def websocket(request):
    return web.json_response({})
