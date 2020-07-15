from abc import ABC, abstractmethod


class AbstractField(ABC):

    @abstractmethod
    def set_value(self, value):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def view(self):
        pass

