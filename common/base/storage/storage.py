from common.abs.storage.storage import AbstractDictionary, AbstractMultiDictionary, AbstractList, \
    AbstractMultiList, AbstractStorage
from common.base.serilizer.serilizer import Serializer
from core.redis.conection import ConnectionSupplier
from utils.oop import classproperty


class Storage(AbstractStorage):
    class Meta:
        abstract = True

    @classmethod
    def unique_id(cls, unique):
        return unique

    @classmethod
    async def get_redis(cls):
        return await ConnectionSupplier.get_redis(cls.name)

    @classproperty
    def name(cls):
        meta = getattr(cls, 'Meta', None)
        if meta is None:
            return cls.__name__
        else:
            return getattr(meta, 'name', cls.__name__)


class SerializeDictionary(Storage, AbstractDictionary):
    serializer = Serializer

    class Meta:
        abstract = True

    @classmethod
    def unique_id(cls, unique=None):
        return cls.name

    @classmethod
    async def get(cls, key):
        if key is None:
            raise TypeError("key can't be None")
        redis = await cls.get_redis()
        key = cls.serializer.key_serialize(key)
        res = await redis.hget(cls.unique_id(), key)
        if res is None:
            return None
        return cls.serializer.value_deserialize(res)

    @classmethod
    async def set(cls, key, value):
        if key is None:
            raise TypeError("key can't be None")
        redis = await cls.get_redis()
        key = cls.serializer.key_serialize(key)
        value = cls.serializer.value_serialize(value)
        res = await redis.hset(cls.unique_id(), key, value)
        return res

    @classmethod
    async def get_or_set(cls, key, value):
        tmp = await cls.get(key)
        if tmp is None:
            await cls.set(key, value)
            return value
        else:
            return tmp

    @classmethod
    async def remove(cls, key):
        if key is None:
            raise TypeError("key can't be None")
        redis = await cls.get_redis()
        key = cls.serializer.key_serialize(key)
        return await redis.hdel(cls.unique_id(), key)

    @classmethod
    async def default(cls, key, default):
        tmp = await cls.get(key)
        if tmp is None:
            return default
        else:
            return tmp

    @classmethod
    async def mget(cls, *keys):
        redis = await cls.get_redis()
        tmp = await redis.hmget(cls.unique_id(), *keys)
        return [cls.serializer.value_deserialize(value) for value in tmp if value is not None]

    @classmethod
    async def mset(cls, **pairs):
        redis = await cls.get_redis()
        tr = redis.multi_exec()
        for key, value in pairs.items():
            tr.hset(cls.unique_id(), cls.serializer.key_serialize(key), cls.serializer.value_serialize(value))
        await tr.execute()

    @classmethod
    async def exist(cls, key):
        if key is None:
            raise AttributeError("key can`t br None")
        redis = await cls.get_redis()
        return await redis.hexists(cls.unique_id(), key)

    @classmethod
    async def keys(cls):
        redis = await cls.get_redis()
        return [cls.serializer.key_deserialize(el) for el in await redis.hkeys(cls.unique_id())]

    @classmethod
    async def values(cls):
        redis = await cls.get_redis()
        return [cls.serializer.value_deserialize(el) for el in await redis.hvals(cls.unique_id())]

    @classmethod
    async def all(cls):
        return dict(zip(await cls.keys(), await cls.values()))

    @classmethod
    async def clear(cls):
        redis = await cls.get_redis()
        keys = await redis.hkeys(cls.unique_id())
        if not keys:
            return
        await redis.hdel(cls.unique_id(), *keys)

    @classmethod
    async def count(cls):
        redis = await cls.get_redis()
        return await redis.hlen(cls.unique_id())


class SerializeMultiDictionary(Storage, AbstractMultiDictionary):
    serializer = Serializer

    class Meta:
        abstract = True

    @classmethod
    def unique_id(cls, unique):
        return f'{cls.name}:{unique}'

    @classmethod
    async def get(cls, unique, key):
        if key is None:
            raise TypeError("key can't be None")
        redis = await cls.get_redis()
        key = cls.serializer.key_serialize(key)
        res = await redis.hget(cls.unique_id(unique), key)
        if res is None:
            return None
        return cls.serializer.value_deserialize(res)

    @classmethod
    async def set(cls, unique, key, value):
        if key is None:
            raise TypeError("key can't be None")
        redis = await cls.get_redis()
        key = cls.serializer.key_serialize(key)
        value = cls.serializer.value_serialize(value)
        res = await redis.hset(cls.unique_id(unique), key, value)
        return res

    @classmethod
    async def get_or_set(cls, unique, key, value):
        tmp = await cls.get(unique, key)
        if tmp is None:
            await cls.set(unique, key, value)
            return value
        else:
            return tmp

    @classmethod
    async def remove(cls, unique, key):
        if key is None:
            raise TypeError("key can't be None")
        redis = await cls.get_redis()
        key = cls.serializer.key_serialize(key)
        return await redis.hdel(cls.unique_id(unique), key)

    @classmethod
    async def default(cls, unique, key, default):
        tmp = await cls.get(unique, key)
        if tmp is None:
            return default
        else:
            return tmp

    @classmethod
    async def mget(cls, unique, *keys):
        redis = await cls.get_redis()
        tmp = await redis.hmget(cls.unique_id(unique), *keys)
        return [cls.serializer.value_deserialize(value) for value in tmp if value is not None]

    @classmethod
    async def mset(cls, unique, **pairs):
        redis = await cls.get_redis()
        tr = redis.multi_exec()
        for key, value in pairs.items():
            tr.hset(cls.unique_id(unique), cls.serializer.key_serialize(key),
                    cls.serializer.value_serialize(value))
        await tr.execute()

    @classmethod
    async def exist(cls, unique, key):
        if key is None:
            raise AttributeError("key can`t br None")
        redis = await cls.get_redis()
        return await redis.hexists(cls.unique_id(unique), key)

    @classmethod
    async def keys(cls, unique):
        redis = await cls.get_redis()
        return [cls.serializer.key_deserialize(el) for el in await redis.hkeys(cls.unique_id(unique))]

    @classmethod
    async def values(cls, unique):
        redis = await cls.get_redis()
        return [cls.serializer.value_deserialize(el) for el in await redis.hvals(cls.unique_id(unique))]

    @classmethod
    async def all(cls, unique):
        return dict(zip(await cls.keys(unique), await cls.values(unique)))

    @classmethod
    async def clear(cls, unique):
        redis = await cls.get_redis()
        keys = await redis.hkeys(cls.unique_id(unique))
        if not keys:
            return
        await redis.hdel(cls.unique_id(unique), *keys)

    @classmethod
    async def count(cls, unique):
        redis = await cls.get_redis()
        return int(await redis.hlen(cls.unique_id(unique)))


class SerializeList(Storage, AbstractList):
    serializer = Serializer

    class Meta:
        abstract = True

    @classmethod
    def unique_id(cls, unique=None):
        return cls.name

    @classmethod
    async def get(cls, index: int):
        redis = await cls.get_redis()
        return cls.serializer.value_deserialize(await redis.lindex(cls.unique_id(), index))

    @classmethod
    async def push(cls, element):
        redis = await cls.get_redis()
        await redis.rpush(cls.unique_id(), cls.serializer.value_serialize(element))

    @classmethod
    async def insert(cls, element, index: int):
        redis = await cls.get_redis()
        await redis.linsert(cls.unique_id(), cls.serializer.value_serialize(element))

    @classmethod
    async def set(cls, element, index: int):
        redis = await cls.get_redis()
        await redis.lset(cls.unique_id(), cls.serializer.value_serialize(element), index)

    @classmethod
    async def pop(cls):
        redis = await cls.get_redis()
        return cls.serializer.value_deserialize(await redis.lpop(cls.unique_id()))

    @classmethod
    async def slice(cls, start, stop):
        redis = await cls.get_redis()
        return [cls.serializer.key_deserialize(el) for el in await redis.lrange(cls.unique_id(), start, stop)]

    @classmethod
    async def len(cls):
        redis = await cls.get_redis()
        return int(await redis.llen(cls.unique_id()))

    @classmethod
    async def clear(cls):
        redis = await cls.get_redis()
        tr = redis.multi_exec()
        for _ in range(await cls.len()):
            tr.lpop(cls.unique_id())
        await tr.execute()

    @classmethod
    async def as_list(cls):
        return await cls.slice(0, await cls.len() - 1)


class SerializeMultiList(Storage, AbstractMultiList):
    serializer = Serializer

    class Meta:
        abstract = True

    @classmethod
    def unique_id(cls, unique):
        return f'{cls.name}:{unique}'

    @classmethod
    def _format_key(cls, unique):
        return cls.unique_id(cls.serializer.key_serialize(unique))

    @classmethod
    async def get(cls, key, index: int):
        redis = await cls.get_redis()
        return cls.serializer.value_deserialize(await redis.lindex(cls._format_key(key), index))

    @classmethod
    async def push(cls, key, element):
        redis = await cls.get_redis()
        await redis.rpush(cls._format_key(key), cls.serializer.value_serialize(element))

    @classmethod
    async def insert(cls, key, element, index: int):
        redis = await cls.get_redis()
        await redis.linsert(cls._format_key(key), cls.serializer.value_serialize(element))

    @classmethod
    async def set(cls, key, element, index: int):
        redis = await cls.get_redis()
        await redis.lset(cls._format_key(key), cls.serializer.value_serialize(element), index)

    @classmethod
    async def pop(cls, key):
        redis = await cls.get_redis()
        return cls.serializer.value_deserialize(await redis.lpop(cls._format_key(key)))

    @classmethod
    async def slice(cls, key, start, stop):
        redis = await cls.get_redis()
        return [cls.serializer.key_deserialize(el) for el in await redis.lrange(start, stop)]

    @classmethod
    async def len(cls, key):
        redis = await cls.get_redis()
        return int(await redis.llen(cls._format_key(key)))

    @classmethod
    async def clear(cls, key):
        redis = await cls.get_redis()
        tr = redis.multi_exec()
        for _ in range(await cls.len(key)):
            tr.lpop(cls._format_key(key))
        await tr.execute()

    @classmethod
    async def as_list(cls, key):
        return await cls.slice(cls._format_key(key), 0, await cls.len(key))


def storage_generator(klass: type):
    def generator(name: str, serializer=Serializer):
        try:
            meta = type('Meta', (object,), {'abstract': False, 'name': name})
            return type(f'Generated{klass.__name__}', (klass,), {'Meta': meta, 'serializer': serializer})
        except Exception:
            raise AttributeError('wrong name')
    return generator


serialize_dictionary = storage_generator(SerializeDictionary)
serialize_mdictionary = storage_generator(SerializeMultiDictionary)
serialize_list = storage_generator(SerializeList)
serialize_mlist = storage_generator(SerializeMultiList)