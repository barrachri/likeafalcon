"""Event watchers."""

from rampante import subscribe_on
from app.models import Event
import logging

log = logging.getLogger(__name__)

@subscribe_on("like.a.falcon")
async def add_new_event(topic, event, app):
    query = Event.insert().values(
            data=event
        )
    async with app['db'].acquire() as conn:
        await conn.execute(query)
    log.info("Message received!")
