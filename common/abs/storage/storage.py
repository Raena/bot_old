from abc import ABC, abstractmethod, ABCMeta

from core.redis.conection import Registrar
from utils.oop import classproperty


class AbstractStorage(metaclass=type('ABC_Registrar', (Registrar, ABCMeta), {})):
    class Meta:
        abstract = True

    @classproperty
    @abstractmethod
    def name(cls):
        pass

    @classmethod
    @abstractmethod
    async def get_redis(cls):
        pass

    @classmethod
    @abstractmethod
    def unique_id(cls, unique):
        pass


class AbstractDictionary:

    @classmethod
    @abstractmethod
    async def set(cls, key, value):
        pass

    @classmethod
    @abstractmethod
    async def get(cls, key):
        pass

    @classmethod
    @abstractmethod
    async def get_or_set(cls, key, value):
        pass

    @classmethod
    @abstractmethod
    async def remove(cls, key):
        pass

    @classmethod
    @abstractmethod
    async def default(cls, key, default):
        pass

    @classmethod
    @abstractmethod
    async def mget(cls, *keys):
        pass

    @classmethod
    @abstractmethod
    async def mset(cls, **pairs):
        pass

    @classmethod
    @abstractmethod
    async def exist(cls, key):
        pass

    @classmethod
    @abstractmethod
    async def keys(cls):
        pass

    @classmethod
    @abstractmethod
    async def values(cls):
        pass

    @classmethod
    @abstractmethod
    async def all(cls):
        pass

    @classmethod
    @abstractmethod
    async def clear(cls):
        pass

    @classmethod
    @abstractmethod
    async def count(cls):
        pass


class AbstractMultiDictionary:

    @classmethod
    @abstractmethod
    async def set(cls, unique, key, value):
        pass

    @classmethod
    @abstractmethod
    async def get(cls, unique, key):
        pass

    @classmethod
    @abstractmethod
    async def get_or_set(cls, unique, key, value):
        pass

    @classmethod
    @abstractmethod
    async def remove(cls, unique, key):
        pass

    @classmethod
    @abstractmethod
    async def default(cls, unique, key, default):
        pass

    @classmethod
    @abstractmethod
    async def mget(cls, unique, *keys):
        pass

    @classmethod
    @abstractmethod
    async def mset(cls, unique, **pairs):
        pass

    @classmethod
    @abstractmethod
    async def exist(cls, unique, key):
        pass

    @classmethod
    @abstractmethod
    async def keys(cls, unique):
        pass

    @classmethod
    @abstractmethod
    async def values(cls, unique):
        pass

    @classmethod
    @abstractmethod
    async def all(cls, unique):
        pass

    @classmethod
    @abstractmethod
    async def clear(cls, unique):
        pass

    @classmethod
    @abstractmethod
    async def count(cls, unique):
        pass


class AbstractList:

    @classmethod
    @abstractmethod
    async def get(cls, index: int):
        pass

    @classmethod
    @abstractmethod
    async def push(cls, element):
        pass

    @classmethod
    @abstractmethod
    async def insert(cls, element, index: int):
        pass

    @classmethod
    @abstractmethod
    async def set(cls, element, index: int):
        pass

    @classmethod
    @abstractmethod
    async def pop(cls):
        pass

    @classmethod
    @abstractmethod
    async def slice(cls, start, stop):
        pass

    @classmethod
    @abstractmethod
    async def len(cls):
        pass

    @classmethod
    @abstractmethod
    async def clear(cls):
        pass

    @classmethod
    @abstractmethod
    async def as_list(cls):
        pass


class AbstractMultiList:

    @classmethod
    @abstractmethod
    async def get(cls, key, index: int):
        pass

    @classmethod
    @abstractmethod
    async def push(cls, key, element):
        pass

    @classmethod
    @abstractmethod
    async def insert(cls, key, element, index: int):
        pass

    @callable
    @abstractmethod
    async def set(self, key, element, index: int):
        pass

    @classmethod
    @abstractmethod
    async def pop(cls, key):
        pass

    @classmethod
    @abstractmethod
    async def slice(cls, key, start, stop):
        pass

    @classmethod
    @abstractmethod
    async def len(cls, key):
        pass

    @classmethod
    @abstractmethod
    async def clear(cls, key):
        pass

    @classmethod
    @abstractmethod
    async def as_list(cls, key):
        pass
