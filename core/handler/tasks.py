from core.navigation.navigator import Navigator
from session.session import Session
from enums.event import EventType
from bot.loop import get_loop
import asyncio


class ChannelQueue:
    _queues = dict()
    _lock = asyncio.Lock()

    @classmethod
    async def get(cls, channel_id) -> asyncio.Queue:
        if cls._queues.get(channel_id) is None:
            cls._queues[channel_id] = asyncio.Queue()
            get_loop().create_task(handler(channel_id))
        return cls._queues[channel_id]

    @classmethod
    async def delete(cls, channel_id):
        del cls._queues[channel_id]


async def handler(channel_id):
    queue = await ChannelQueue.get(channel_id)
    while True:
        future = asyncio.ensure_future(queue.get())
        try:
            item = await asyncio.wait_for(future, timeout=10, loop=get_loop())
            await item
        except asyncio.TimeoutError:
            return await ChannelQueue.delete(channel_id)


async def handle(context, session):
    application = Navigator.get(await session.get_path())
    queue = await ChannelQueue.get(session.channel_id)
    permissions = await application.permissions(session)
    channel_types = await application.channel_types()
    # TODO делать проверку, может ли пользователь использовать приложение.
    context['session'] = session
    if not await session.application_started():
        await queue.put(application.begin(session))
        await queue.put(application.run(context))
    else:
        await queue.put(application.run(context))


async def event_handler(context):
    user_id = None
    channel_id = None
    if context['type'] in {EventType.MESSAGE_EDIT}:
        user_id = context['after'].author.id
        channel_id = context['after'].channel.id
    elif context['type'] in {EventType.MESSAGE_NEW, EventType.MESSAGE_DELETE}:
        user_id = context['message'].author.id
        channel_id = context['message'].channel.id

    elif context['type'] in {EventType.REACTION_ADD, EventType.REACTION_REMOVE}:
        user_id = context['user'].id
        channel_id = context['reaction'].message.channel.id
    session = Session(user_id, channel_id)
    return await handle(context, session)
