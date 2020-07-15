from bot.client import get_client
from common.base.app.application import Application
from session.session import Session


class ExampleApplication(Application):

    @classmethod
    async def on_start(cls, session: Session):
        channel = get_client().get_channel(session.channel_id)
        await channel.send('example started')

    @classmethod
    async def run(cls, ctx):
        pass

    @classmethod
    async def on_finish(cls, session: Session):
        pass
