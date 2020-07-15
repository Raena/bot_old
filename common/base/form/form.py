from common.abs.form.form import AbstractForm
from common.base.field.field import Field
from common.base.gui.window import Window, WindowData
import copy


class DeclarativeFieldsMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                current_fields.append((key, value))
                attrs.pop(key)
        attrs['declared_fields'] = dict(current_fields)

        new_class = super(DeclarativeFieldsMetaclass, mcs).__new__(mcs, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = {}
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, 'declared_fields'):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class


class BaseForm(AbstractForm):

    base_fields = None

    def __init__(self, title, description):
        self.fields = copy.deepcopy(self.base_fields)
        self.title = title
        self.description = description
        fields = []
        for num, field in enumerate(self.fields):
            fields.append({'name': field[1].verbose_name or field[0], 'value': f'{num + 1} {field[1].view()}'})
        window_data = WindowData(title=title, description=description, fields=fields)
        self.window = Window(window_data)

    def is_valid(self):
        pass

    def get_gui(self):
        return self.window

    def clean(self):
        pass

    def __getitem__(self, item):
        for field in self.fields:
            if field[0] == item:
                return field[1].value
        else:
            raise KeyError('No such filed')


class Form(BaseForm, DeclarativeFieldsMetaclass):
    pass
