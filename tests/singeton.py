from sqlalchemy import Column, Integer, String
from common.base.model.model import Model


# объявление модели пользователя
class User(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


# Создание объекта User с автоматическим сохранинием записи в бд.
user1 = await User.create(name='Andrew', age=80)

# Создание объекта User, без сохранения.
user2 = User(name='Bob', age=32)

# Явное сохрание в бд.
await user2.save()
