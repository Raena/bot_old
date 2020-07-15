from abc import abstractmethod, ABC


class AbstractSingleton(ABC):

    _data = None

    @classmethod
    @abstractmethod
    def initial(cls):
        pass

    @classmethod
    @abstractmethod
    def get(cls):
        pass

    @classmethod
    @abstractmethod
    def set(cls, value):
        pass