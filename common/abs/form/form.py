from abc import ABC, abstractmethod


class AbstractForm(ABC):

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def get_gui(self):
        pass

    @abstractmethod
    def clean(self):
        pass
