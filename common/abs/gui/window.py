from abc import ABC, abstractmethod, abstractproperty
import discord


class AbstractWindowData(ABC):

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def fields(self):
        pass

    @property
    @abstractmethod
    def color(self):
        pass

    @property
    @abstractmethod
    def footer(self):
        pass

    @property
    @abstractmethod
    def reactions(self):
        pass

    @title.setter
    @abstractmethod
    def title(self, value):
        pass

    @description.setter
    @abstractmethod
    def description(self, value):
        pass

    @fields.setter
    @abstractmethod
    def fields(self, value):
        pass

    @color.setter
    @abstractmethod
    def color(self, value):
        pass

    @footer.setter
    @abstractmethod
    def footer(self, value):
        pass

    @reactions.setter
    @abstractmethod
    def reactions(self, value):
        pass


class AbstractWindow(ABC):

    @abstractmethod
    async def send(self, channel: discord.abc.Messageable):
        pass

    @abstractmethod
    async def delete(self):
        pass

    @abstractmethod
    async def update(self):
        pass

    @abstractmethod
    async def reaction(self, reaction):
        pass
