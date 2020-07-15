from asyncio import Lock
from abc import ABC, abstractmethod


class AbstractAsyncSingleton(ABC):
    _data = None
    _lock = None

    @classmethod
    @abstractmethod
    def get_lock(cls) -> Lock:
        pass

    @classmethod
    @abstractmethod
    async def initial(cls):
        pass

    @classmethod
    @abstractmethod
    async def get(cls) -> type(_data):
        pass

    @classmethod
    @abstractmethod
    async def set(cls, value):
        pass
