from aiohttp import web
from rampante import streaming
from app.models import Event
from sqlalchemy import select
from app.serializers import EventSchema
import aiohttp
from json import JSONDecodeError
import os
from config import Config as C

async def index(request):
    """Return a html page where you can get updates through ws."""
    WS_FILE = os.path.join(C.BASE, 'templates/websocket.html')
    print(WS_FILE)
    with open(WS_FILE, 'rb') as fp:
        return web.Response(body=fp.read(), content_type='text/html')


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


async def websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                request.app['websockets'].discard(ws)
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws
