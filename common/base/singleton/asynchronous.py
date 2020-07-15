from asyncio.locks import Lock
from abc import abstractmethod

from common.abs.singleton.asynchronous import AbstractAsyncSingleton


class AsyncSingleton(AbstractAsyncSingleton):

    @classmethod
    @abstractmethod
    async def initial(cls):
        pass

    @classmethod
    def get_lock(cls) -> Lock:
        if cls._lock is None:
            cls._lock = Lock()
        return cls._lock

    @classmethod
    async def get(cls):
        lock = cls.get_lock()
        async with lock:
            if cls._data is None:
                cls._data = await cls.initial()
            res = cls._data
        return res

    @classmethod
    async def set(cls, value):
        lock = cls.get_lock()
        async with lock:
            cls._data = value
