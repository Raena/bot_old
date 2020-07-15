from common.base.singleton.sinchronous import Singleton
from bot.loop import get_loop
import discord
from utils.oop import classproperty


class DiscordClient(Singleton):

    @classmethod
    def initial(cls):
        return discord.Client(loop=get_loop())

    @classproperty
    def id(cls):
        return cls.get().user.id

    @classproperty
    def user(cls):
        return cls.get().user


def get_client() -> discord.Client:
    return DiscordClient.get()
