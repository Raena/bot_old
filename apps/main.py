from common.base.app.application import Application
from session.session import Session
from bot.client import get_client


class App(Application):
    @classmethod
    async def run(cls, response):
        session = response['session']
        return await cls.cd(session, 'example')

    @classmethod
    async def on_start(cls, session: Session):
        chanel = get_client().get_channel(session.channel_id)
        await chanel.send("`StartApp started`")

    @classmethod
    async def on_finish(cls, session: Session):
        chanel = get_client().get_channel(session.channel_id)
        await chanel.send("`StartApp finished`")
