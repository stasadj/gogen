import os
from datetime import datetime
from silvera.core import TypedList, TypeDef


def get_root_path():
    """Returns project's root path."""
    path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    return path


def get_templates_path():
    """Returns the path to the templates folder."""
    return os.path.join(get_root_path(), "gogen", "templates")


def timestamp():
    return "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())


def create_if_missing(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


GO_TYPES = {
    'str': 'string',
    'float': 'float32',
    'double': 'float32',
    'bool': 'bool',
    'int': 'int',
    'i16': 'int16',
    'i31': 'int32',
    'i64': 'int64'
}


def convert_complex_type(x):
    if isinstance(x, TypedList):
        type = x.type.name if isinstance(x.type, TypeDef) else x.type
        return '[]' + GO_TYPES.get(type, type)
    return GO_TYPES.get(x, x)
