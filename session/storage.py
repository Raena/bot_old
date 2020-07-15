import asyncio
from session.serializer import SessionSerializer
from common.base.storage.storage import SerializeDictionary
from common.base.storage.storage import SerializeMultiDictionary
from common.base.singleton.asynchronous import AsyncSingleton


class SessionDirectoryDictionary(SerializeDictionary):
    serializer = SessionSerializer

    @classmethod
    async def get(cls, key):
        value = await super().get(key)
        if value is None:
            return '/'
        return value

    class Meta:
        name = 'DirectorySessionDictionary'
        abstract = False


class PyObjDict(AsyncSingleton):
    @classmethod
    async def initial(cls):
        return {}


class SessionSysDataDictionary(SerializeMultiDictionary):
    class Meta:
        name = 'session_sys_data'
        db = 2
        abstract = False


class SessionDictionary(SerializeMultiDictionary):
    class Meta:
        name = 'session_data'
        db = 2
        abstract = False

    _py_obj_storage = PyObjDict

    @classmethod
    def primitive_type(cls, value):
        return isinstance(value, (int, str, float, bytes, bytearray, bool))

    @classmethod
    async def get(cls, unique, key):
        storage = await cls._py_obj_storage.get()
        if f"{unique}:{key}" not in storage:
            return await super().get(unique, key)
        else:
            return storage.get(f"{unique}:{key}")

    @classmethod
    async def set(cls, unique, key, value):
        storage = await cls._py_obj_storage.get()
        if cls.primitive_type(value):
            return await super().set(unique, key, value)
        else:
            storage[f"{unique}:{key}"] = value

    @classmethod
    async def remove(cls, unique, key):
        storage = await cls._py_obj_storage.get()
        if f"{unique}:{key}" not in storage:
            return await super().remove(unique, key)
        else:
            return storage.pop(f"{unique}:{key}")

    @classmethod
    async def default(cls, unique, key, default):
        storage = await cls._py_obj_storage.get()
        if f"{unique}:{key}" in storage:
            return storage.get(f"{unique}:{key}", default)
        else:
            return await super().default(unique, key, default)

    @classmethod
    async def mget(cls, unique, *keys):
        values = await super().mget(unique, *keys)
        storage = await cls._py_obj_storage.get()
        for key in storage:
            if f"{unique}:{key}" in storage:
                values.append(storage.get(f"{unique}:{key}"))
        return values

    @classmethod
    async def mset(cls, unique, **pairs):
        for key, value in pairs.items():
            await cls.set(unique, key, value)

    @classmethod
    async def exist(cls, unique, key):
        storage = await cls._py_obj_storage.get()
        return f"{unique}:{key}" in storage or await super().exist(unique, key)

    @classmethod
    async def keys(cls, unique):
        storage = await cls._py_obj_storage.get()
        keys = [el.split(':')[1] for el in storage.keys() if el.split(':')[0] == str(unique)]
        keys.extend(await super().keys(unique))
        return keys

    @classmethod
    async def values(cls, unique):
        storage = await cls._py_obj_storage.get()
        values = list(storage.values())
        values.extend(await super().values(unique))
        return values

    @classmethod
    async def all(cls, unique):
        storage = await cls._py_obj_storage.get()
        _all = {}
        for key, value in storage.items():
            if key.split(':'[0]) == str(unique):
                _all[key.split(':'[1])] = value

        _all.update(await super().all(unique))
        return _all

    @classmethod
    async def clear(cls, unique):
        storage = await cls._py_obj_storage.get()
        for key in storage:
            if key.split(':'[0]) == str(unique):
                del storage[key]
        await super().clear(unique)

    @classmethod
    async def count(cls, unique):
        return len(await cls.keys(unique))
