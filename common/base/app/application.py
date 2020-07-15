from common.abs.app.application import AbstractApplication
from core.navigation.navigator import Navigator
from session.session import Session
from settings import APPLICATION_MODULE
from enums.permissions import Permission
from enums.channel import ChannelType


class Application(AbstractApplication):

    @classmethod
    async def permissions(cls, session: Session) -> tuple:
        """
        должен возвращать, то, какими правами должен обладать пользователь, чтобы использовать это приложание.
        """
        return Permission.ALL,

    @classmethod
    async def channel_types(cls) -> tuple:
        """
        возвраащет список типов каналов в которых может работать это приложение.
        """
        return ChannelType.All,

    @classmethod
    async def run(cls, ctx: dict):
        """
            Основной метод, обрабатывающий новые события от пользователя.
        """
        return

    @classmethod
    async def begin(cls, session):
        await session.application_start()
        await cls.on_start(session)

    @classmethod
    async def destroy(cls, session):
        await cls.on_finish(session)
        await session.application_finish()

    @classmethod
    async def on_start(cls, session: Session):
        """
            Метод, вызываемый при переходе в новое приложение командой cd.
            Следует использовать для подгрузки клавиатуры и базового меню нового окна.
        """
        return

    @classmethod
    async def on_finish(cls, session: Session):
        """
            Метод, вызываемый при завершении работы с приложением вызывается при переходи в новое приложение.
            Завершает выполнение текущего приложение.
        """
        return

    @classmethod
    async def pwd(cls) -> str:
        """
            Показать текущую дирректорию, где находится этот класс
            Корневой папкой считается APPLICATION_PATH
        """
        result = cls.__module__.replace(APPLICATION_MODULE, '', 1).strip('.')
        ind = result.rfind('.')
        if ind >= 0:
            result = result[:ind]
        else:
            result = ''
        if result == '':
            result = '/'
        return result

    @classmethod
    async def dir(cls) -> list:
        """
            Показать приложения, которые находятся в вашей директории с модулем.
            Если вы хотите изменить доступ некоторым пользователям к этой директории,
            Переопределите метод в вашем пакете, вызовите dir супер класса и измените доступный список директорий.
        """
        return Navigator.dir(await cls.pwd())

    @classmethod
    async def cd(cls, session: Session, path: str) -> bool:
        """
            Переидти к модулю по пути cd_path.
            Если начинается с '/', путь глобальный, можно использовать любую длину и вложеность
            Если начинается с имени модуля, путь локальный, берётся один из модулей в dir().
            Также можно вернуться к предыдущему модулю командой 'cd ..'
            Составные команды не принимаются ввиду отсутствия парсера.
        """
        if path == '/':
            await cls._start_new_app(session, '/')
            return True

        path = path.strip('/')

        if path == '..':
            user_path = await cls.pwd()
            if user_path != '/':
                path = user_path.strip('/.')
                ind = path.rfind('.')
                if ind >= 0:
                    path = path[:ind]
                if path == '':
                    path = '/'
                await cls._start_new_app(session, path)
                return True
            else:
                return False

        if not path.startswith('/'):
            user_path = await cls.pwd()
            if not user_path.endswith('/'):
                user_path += '/'
            user_path += path
            path = user_path

        package_split_point = path.rfind('/')
        if str(path[package_split_point + 1:]).strip() in Navigator.dir(path[:package_split_point]):
            await cls._start_new_app(session, path.strip('.'))
            return True
        else:
            return False

    @classmethod
    async def _start_new_app(cls, session: Session, app_path: str):
        await cls.destroy(session)
        await session.set_path(app_path)
        await Navigator.get(app_path).begin(session)
