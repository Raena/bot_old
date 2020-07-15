import inspect
import importlib
from os import listdir
from os.path import isdir, isfile, join
from settings import APPLICATION_DIR, APPLICATION_MODULE
from common.abs.app.application import AbstractApplication


class Navigator:

    @classmethod
    def get(cls, path: str):
        if path.startswith('/'):
            path = path[1:]
        classes = cls.dir_classes(path)
        for spec_class in classes:
            try:
                target_path = path if path != '' else path + '/'
                target = cls.get_class_from_module(target_path.strip('.') + '.' + spec_class.strip('.'))
            except Exception as e:
                raise e
            else:
                return target
        raise Exception('Не найден класс-наследник Application в данной директории\n'
                        + 'Проверьте правильность пути и его содержимое ' +
                        f'{APPLICATION_DIR + "/" + path}')

    @classmethod
    def dir(cls, path: str):
        if path.startswith('/'):
            path = path[1:]
        path = '{0}/{1}'.format(APPLICATION_DIR, path.replace('.', '/'))
        only_pkg = [f for f in listdir(path) if isdir(join(path, f)) and not f.startswith('_')]
        return only_pkg

    @classmethod
    def dir_classes(cls, path: str):
        if path.startswith('/'):
            path = path[1:]
        path = '{0}/{1}'.format(APPLICATION_DIR, path.replace('.', '/'))
        return [f.replace('.py', '') for f in listdir(path) if isfile(join(path, f)) and f.endswith('.py')]

    @classmethod
    def get_class_from_module(cls, path: str):
        path = (APPLICATION_MODULE + '.' + path.replace('/', '.').strip('.')).strip('.')
        module = importlib.import_module(path)
        cls_members = inspect.getmembers(module, inspect.isclass)
        target = None
        max_count = 0
        for cls_member in cls_members:
            children = cls_member[1]
            if AbstractApplication in children.__mro__:
                if len(children.__mro__) > max_count:
                    target = children
                    max_count = len(children.__mro__)
        if target is None:
            raise Exception(
                'Не пройдён флаг безопасности, проверьте правильность наследования класса {0}'.format(cls_members))

        return target
