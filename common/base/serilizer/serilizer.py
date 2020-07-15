from common.abs.serilizer.serializer import AbstractSerializer


class Serializer(AbstractSerializer):

    @classmethod
    def key_deserialize(cls, key: bytes):
        return key.decode('utf-8')

    @classmethod
    def key_serialize(cls, key):
        return str(key)

    @classmethod
    def value_serialize(cls, value):
        return str(value)

    @classmethod
    def value_deserialize(cls, value: bytes):
        return value.decode('utf-8')
