from common.base.app.application import Application
from enums.event import EventType
from session.session import Session


class ExampleApplication(Application):

    @classmethod
    async def on_start(cls, session: Session):
        # вызываемый перед началом обработки метод

        # получение канала из сессии
        channel = session.get_discord_channel()

        # отправляем сообщение пользователю, что приложение запучтилось.
        await channel.send('example started')

    @classmethod
    async def run(cls, ctx):
        # вызывается на каждое события пользователя при активном приложении

        # получим тип события
        event_type = ctx['type']

        # получим сессию
        session = ctx['session']

        # получим значения счётчика или, если счётчика ещё нет, то создим его со значением 0
        count = await session.get_or_set('count', 0)

        # в зависимости от типа события произвидём действия
        if event_type == EventType.MESSAGE_NEW:
            print(f'Полученно новой сообщение от пользователя: {ctx["message"].content}')
        elif event_type == EventType.MESSAGE_EDIT:
            print(f'пользователь редатировал сообщение: {ctx["before"].id}')
        elif event_type == EventType.REACTION_ADD:
            print(f'пользователь добавил реакцию')

        count += 1

        if count > 4:
            print('пользователь совершил 4 действия')

            # если пльзователь совершил более 3 трёх действий передём в главное приложение.
            await cls.cd(session, '/')

    @classmethod
    async def on_finish(cls, session: Session):
        # я вызовусь при заврешении

        # очистим тут сессию от записанных данных (избавимся от count)
        await session.clear()
