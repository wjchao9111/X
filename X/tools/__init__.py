import importlib
import random
import string
import time

from X.tools.log import log


class Factory:
    def __init__(self):
        pass

    class_dict = {}
    inst_dict = {}

    @staticmethod
    def load(path, *args, **kwargs):
        if path not in Factory.inst_dict:
            Factory.inst_dict[path] = load_class(path, *args, **kwargs)

        return Factory.inst_dict[path]

    @staticmethod
    def load_cls(path):
        try:
            if path not in Factory.class_dict:
                Factory.class_dict[path] = load_cls(path)

            return Factory.class_dict[path]
        except:
            log(
                title='LOAD_CLS_EXCEPTION_%s' % path,
                content=None,
                logger='sms',
                level='error'
            )
            return None


def load_class(path, *args, **kwargs):
    cls = load_cls(path)
    return cls(*args, **kwargs)


def load_cls(path):
    path = path.split('.')
    class_name = path[-1]
    class_path = '.'.join(path[:-1])
    module = importlib.import_module(class_path)
    cls = getattr(module, class_name)
    return cls


class LoaderCache:
    app_set = {}

    def __init__(self, delay=1):
        self.delay = delay
        self.result_set = {}

    @staticmethod
    def set(app, key, value, delay=10):
        now = time.time()
        result = {'exp_time': now + delay, 'value': value}
        if app not in LoaderCache.app_set:
            LoaderCache.app_set[app] = {}
        result_set = LoaderCache.app_set.get(app)
        result_set[key] = result

    @staticmethod
    def empty_key():
        result = {'exp_time': 0, 'value': None}
        return result

    @staticmethod
    def get(app, key):
        result_set = LoaderCache.app_set.get(app, {})
        result = result_set.get(key, LoaderCache.empty_key())
        now = time.time()
        if now > result.get('exp_time'):
            valid = False
        else:
            valid = True
        return valid, result.get('value')


def lazy_loader(function):
    def decorator(*args, **kwargs):
        app = function.func_name
        sender = args[0]

        key = len(args) > 1 and args[1] or None

        delay_name = '%s_delay' % app
        if not hasattr(sender, delay_name):
            setattr(sender, delay_name, 10)
        delay = getattr(sender, delay_name)

        valid, value = LoaderCache.get(app, key)
        if not valid:
            value = function(*args, **kwargs)
            LoaderCache.set(app, key, value, delay)
        return value

    return decorator


lazy_delay = 10


def lazy_loader_const(function):
    def decorator(*args, **kwargs):
        app = function.func_name

        key = len(args) > 0 and args[0] or None

        delay = lazy_delay

        valid, value = LoaderCache.get(app, key)
        if not valid:
            value = function(*args, **kwargs)
            LoaderCache.set(app, key, value, delay)
        return value

    return decorator


def get_random_str(str_len=32):
    rule = string.letters + string.digits
    str = random.sample(rule, str_len)
    return "".join(str)


def get_random_num(str_len=32):
    rule = string.digits
    str = random.sample(rule, str_len)
    return "".join(str)
