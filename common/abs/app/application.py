from session.session import Session
from abc import ABC, abstractmethod


class AbstractApplication(ABC):

    @classmethod
    @abstractmethod
    async def permissions(cls, session: Session) -> tuple:
        pass

    @classmethod
    @abstractmethod
    async def channel_types(cls) -> tuple:
        pass

    @classmethod
    @abstractmethod
    async def run(cls, ctx: dict):
        pass

    @classmethod
    @abstractmethod
    async def begin(cls, session):
        pass

    @classmethod
    @abstractmethod
    async def destroy(cls, session):
        pass

    @classmethod
    @abstractmethod
    async def on_start(cls, session: Session):
        pass

    @classmethod
    @abstractmethod
    async def on_finish(cls, session: Session):
        pass

    @classmethod
    @abstractmethod
    async def pwd(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    async def dir(cls) -> list:
        pass

    @classmethod
    @abstractmethod
    async def cd(cls, session: Session, path: str) -> bool:
        pass
