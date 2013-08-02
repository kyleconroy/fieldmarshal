import inspect 
import StringIO
import json


def _get_user_attributes(cls):
    boring = dir(type('dummy', (object,), {}))
    return [item
            for item in inspect.getmembers(cls)
            if item[0] not in boring]


def _default_value(t):
    if t == str:
        return ''
    elif t == bool:
        return False
    elif t == int:
        return 0
    elif t == list:
        return []
    elif t == dict or t == set:
        return {}
    elif type(t) == type and issubclass(t, Struct):
        return t()
    else:
        return None #Bad case


def _dict_load(klass, payload):
    for name, value in _get_user_attributes(klass):
        if name in payload and issubclass(value, Struct):
            payload[name] = _dict_load(value, payload[name])
    return klass(**payload)


def _dict_repr(obj):
    output = {}
    for name, klass in _get_user_attributes(obj.__class__):
        if isinstance(getattr(obj, name), Struct):
            output[name] = _dict_repr(getattr(obj, name))
        else:
            output[name] = getattr(obj, name)
    return output


class Struct(object):

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        for name, klass in _get_user_attributes(self.__class__):
            if name not in kwargs:
                setattr(self, name, _default_value(klass))


def dump(obj, file_object):
    file_object.write(dumps(obj))


def dumps(obj):
    output = {}
    return json.dumps(_dict_repr(obj))


def load(klass, file_object):
    payload = json.load(file_object)
    return _dict_load(klass, payload)


def loads(klass, text):
    return load(klass, StringIO.StringIO(text))



