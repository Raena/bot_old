from common.abs.singleton.sinchronous import AbstractSingleton
from abc import abstractmethod


class Singleton(AbstractSingleton):
    @classmethod
    @abstractmethod
    def initial(cls):
        pass

    @classmethod
    def get(cls):
        if cls._data is None:
            cls._data = cls.initial()
        return cls._data

    @classmethod
    def set(cls, value):
        cls._data = value
