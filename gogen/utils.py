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
    'double': 'float64',
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


from silvera.const import  HTTP_POST


def unfold_function_params(func, with_annotations=True):
    """Creates a string from function parameters
       Args:
           func (Function): function whole params are unfolded
           with_annotations (bool): tells whether special annotations shall be
               included in string or not
       """
    if with_annotations and func.http_verb == HTTP_POST:
        params = func.params
        if len(params) == 1:
            param = params[0]
            param_type = convert_complex_type(param.type)
            return "@RequestBody %s %s" % (param_type, param.name)

    params = []
    for p in func.params:
        param = ""
        if with_annotations:
            if p.url_placeholder:
                param = "@PathVariable "
            elif p.query_param:
                required = "true" if p.default is None else "false"
                param = '@RequestParam(value="%s", required=%s) ' % (p.name,
                                                                         required)
            else:
                param = "@RequestBody "
        param += p.name + " "
        param += convert_complex_type(p.type)
        params.append(param)

    return ", ".join(params)
