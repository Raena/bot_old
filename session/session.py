from session.storage import SessionDictionary
from session.storage import SessionDirectoryDictionary
from session.storage import SessionSysDataDictionary
from bot.client import get_client


class Session:
    storage = SessionDictionary
    path_storage = SessionDirectoryDictionary
    sys_data_storage = SessionSysDataDictionary

    def __init__(self, user_id: int, channel_id: int):
        self.user_id = user_id
        self.channel_id = channel_id

    def __hash__(self):
        return hash((self.user_id, self.channel_id))

    def __eq__(self, other):
        return self.user_id == other.user_id and self.channel_id == other.channel_id

    def __str__(self):
        return f'{self.user_id}:{self.channel_id}'

    def get_discord_user(self):
        return get_client().get_user(self.user_id)

    def get_discord_channel(self):
        return get_client().get_channel(self.channel_id)

    @classmethod
    def dump(cls, session) -> bytes:
        return bytes(f"{session.user_id}|{session.channel_id}")

    @classmethod
    def load(cls, session_dumped: bytes):
        user_id, channel_id = session_dumped.decode('utf-8').split('|')
        return Session(int(user_id), int(channel_id))

    def get_path(self):
        return self.path_storage.get(self)

    def set_path(self, path: str):
        return self.path_storage.set(self, path)

    async def application_started(self):
        answer = await self.sys_data_storage.get(hash(self), 'started')
        return answer == 'yes'

    def application_start(self):
        return self.sys_data_storage.set(hash(self), 'started', 'yes')

    def application_finish(self):
        return self.sys_data_storage.set(hash(self), 'started', 'no')

    def get(self, key):
        return self.storage.get(hash(self), key)

    def set(self, key, value):
        return self.storage.set(hash(self), key, value)

    def get_or_set(self, key, value):
        return self.storage.get_or_set(hash(self), key, value)

    def remove(self, key):
        return self.storage.remove(hash(self), key)

    def default(self, key, default):
        return self.storage.default(hash(self), key, default)

    def mget(self, *keys):
        return self.storage.mget(hash(self), *keys)

    def mset(self, **pairs):
        return self.storage.mset(hash(self), **pairs)

    def exist(self, key):
        return self.storage.exist(hash(self), key)

    def keys(self):
        return self.storage.keys(hash(self))

    def values(self):
        return self.storage.values(hash(self))

    def all(self):
        return self.storage.all(hash(self))

    def clear(self):
        return self.storage.clear(hash(self))

    def count(self):
        return self.storage.count(hash(self))
