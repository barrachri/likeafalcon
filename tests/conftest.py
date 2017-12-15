from aiohttp import web
import pytest
from app import routes

import asyncio
import logging
import logging.config

from aiohttp.test_utils import TestClient, TestServer
from aiopg.sa import create_engine as aiopg_create_engine
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from sqlalchemy_utils.functions import (
    create_database,
    database_exists,
    drop_database,
)
from config import Config as C
from main import (
    add_route,
    start_db_pool,
    stop_db_pool,
    start_task_manager,
    stop_task_manager,
)
from app.models import Event


@pytest.fixture(scope="session")
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop

    # Clean-up
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def test_client(loop):
    clients = []

    async def go(__param, *args, server_kwargs=None, **kwargs):
        server_kwargs = server_kwargs or {}
        server = TestServer(__param, loop=loop, **server_kwargs)
        client = TestClient(server, loop=loop, **kwargs)

        await client.start_server()
        clients.append(client)
        return client

    yield go

    async def finalize():
        while clients:
            await clients.pop().close()

    loop.run_until_complete(finalize())


@pytest.fixture(scope="session")
def create_tables():
    """Create all the tables needed for the test."""
    DB_URI = f'postgresql://{C.DB_USER}:{C.DB_PASSWORD}@{C.DB_HOST}:{C.DB_PORT}/{C.DB_NAME}'
    if database_exists(DB_URI):
        drop_database(DB_URI)
    create_database(DB_URI)
    engine = create_engine(DB_URI)

    conn = engine.connect()
    models = [Event]
    for model in models:
        conn.execute(CreateTable(model).compile(engine).__str__())


@pytest.fixture(scope="session")
def cli(loop, test_client, create_tables):
    app = web.Application()
    add_route(app, *routes)
    # On-startup tasks
    app.on_startup.append(start_task_manager)
    app.on_startup.append(start_db_pool)
    # Clean-up tasks
    app.on_cleanup.append(stop_task_manager)
    app.on_cleanup.append(stop_db_pool)
    # set of ws connection
    app['websockets'] = set()
    return loop.run_until_complete(test_client(app))
