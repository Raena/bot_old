from abc import ABC, abstractmethod


class AbstractModel(ABC):

    @classmethod
    @abstractmethod
    async def create(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def get(cls, *ids):
        pass

    @classmethod
    @abstractmethod
    async def destroy(cls, *ids):
        pass

    @classmethod
    @abstractmethod
    async def find(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def all(cls):
        pass

    @abstractmethod
    async def fill(self, **kwargs):
        pass

    @abstractmethod
    async def update(self, **kwargs):
        pass

    @abstractmethod
    async def save(self):
        pass

    @abstractmethod
    async def delete(self):
        pass
