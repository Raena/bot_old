from common.base.serilizer.serilizer import Serializer


class SessionSerializer(Serializer):

    @classmethod
    def key_serialize(cls, key):
        return hash(key)
