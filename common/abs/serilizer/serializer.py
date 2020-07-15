from abc import ABC, abstractmethod


class AbstractSerializer(ABC):

    @classmethod
    @abstractmethod
    def key_deserialize(cls, key: bytes):
        pass

    @classmethod
    @abstractmethod
    def key_serialize(cls, key) -> str:
        pass

    @classmethod
    @abstractmethod
    def value_serialize(cls, value) -> str:
        pass

    @classmethod
    @abstractmethod
    def value_deserialize(cls, value: bytes):
        pass
