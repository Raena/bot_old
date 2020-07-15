from common.abs.model.model import AbstractModel
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(AbstractModel):
    @classmethod
    async def create(cls, **kwargs):
        pass

    @classmethod
    async def get(cls, *ids):
        pass

    @classmethod
    async def destroy(cls, *ids):
        pass

    @classmethod
    async def find(cls, **kwargs):
        pass

    @classmethod
    async def all(cls):
        pass

    async def fill(self, **kwargs):
        pass

    async def update(self, **kwargs):
        pass

    async def save(self):
        pass

    async def delete(self):
        pass


class Model(BaseModel, Base):
    pass
