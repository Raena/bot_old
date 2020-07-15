from utils.oop import classproperty
import aioredis
import settings as settings
from common.exeptions.storage import StorageException


class Registrar(type):

    def __new__(cls, name, bases, attrs):

        storage_name = name
        abstract = False
        db = 1
        meta = attrs.get('Meta', None)
        if meta is not None:
            storage_name = getattr(meta, 'name', name)
            abstract = getattr(meta, 'abstract', False)
            db = getattr(meta, 'db', 1)
        storage = super().__new__(cls, name, bases, attrs)
        if not abstract:
            try:
                ConnectionSupplier.register_storage(storage_name, storage, db)
            except StorageException as e:
                raise e

        return storage


class ConnectionSupplier:
    _storage = {}
    _redis_pool = None
    _connections = {}

    @classmethod
    async def clear_all(cls):
        return await (await cls.redis_pool())[0].flushall()

    @classmethod
    async def redis_pool(cls):
        if cls._redis_pool is None:
            cls._redis_pool = [await aioredis.create_redis(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", db=i)
                               for i in range(10)]
        return cls._redis_pool

    @classmethod
    async def get_redis(cls, name):
        db = cls._connections.get(name, None)
        if db is None:
            raise StorageException(f"Storage with name '{name}' is not registered")
        redis_pool = await cls.redis_pool()
        return redis_pool[db]

    @classproperty
    def storage(cls):
        return cls._storage

    @classmethod
    def _register(cls, name: str, storage: type, db: int):
        cls._storage[name] = storage
        cls._connections[name] = db

    @classmethod
    def register_storage(cls, name: str, storage: type, db: int):
        if name not in cls.storage:
            if db >= 10:
                raise StorageException(f"Storage max db size is 10, got {db}")
            cls._register(name, storage, db)
        else:
            raise StorageException(f"Exception while registering '{storage.__name__}' Storage with name '{name}' "
                                   f"already exists.")
