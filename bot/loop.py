from asyncio import get_event_loop, AbstractEventLoop
from common.base.singleton.sinchronous import Singleton


class LoopSupplier(Singleton):

    @classmethod
    def initial(cls):
        return get_event_loop()


def get_loop() -> AbstractEventLoop:
    return LoopSupplier.get()
