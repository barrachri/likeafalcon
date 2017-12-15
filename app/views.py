"""Views handlers."""

import logging
import os

import aiohttp
from aiohttp import web

from config import Config as C

log = logging.getLogger(__name__)


async def index(request):
    """Return a websocket page."""
    WS_FILE = os.path.join(C.BASE, 'templates/websocket.html')
    with open(WS_FILE, 'rb') as fp:
        return web.Response(body=fp.read(), content_type='text/html')


async def websocket(request):
    """Websocket to listen on new events."""
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

    log.warning('websocket connection closed')

    return ws
