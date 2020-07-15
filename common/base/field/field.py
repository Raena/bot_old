from common.abs.field.field import AbstractField


class Field(AbstractField):

    def __init__(self, *, description='', verbose_name=''):
        self.description = description
        self.verbose_name = verbose_name
        self.value = None

    def set_value(self, value):
        pass

    def clear(self):
        pass

    def validate(self):
        pass

    def normalize(self):
        pass

    def view(self):
        pass
