def _scan_instance(obj, include_underscore, exclude):
    """(Executed on remote or local engine) Examines an object and returns info
    about any instance-specific methods or attributes.
    (For example, any attributes that were set by __init__() )

    By default, methods or attributes starting with an underscore are ignored.

    Args:
      obj (object): the object to scan. must be on this local engine.
      include_underscore (bool or sequence of str): Should methods or
        attributes that start with an underscore be proxied anyway? If a
        sequence of names is provided then methods or attributes starting with
        an underscore will only be proxied if their names are in the sequence.
      exclude (sequence of str): names of any methods or attributes that should
        not be reported.
    """
    from sys import getsizeof
    always_exclude = ('__new__', '__init__', '__getattribute__', '__class__',
                      '__reduce__', '__reduce_ex__')
    method_info = []
    attributes_info = []
    if hasattr(obj, '__dict__'):
        for name in obj.__dict__:
            if (name not in exclude and 
                name not in always_exclude and
                (name[0] != '_' or 
                 include_underscore is True or
                 name in include_underscore)):
                f = obj.__dict__[name]
                if hasattr(f, '__doc__'):
                    doc = f.__doc__
                else:
                    doc = None
                if callable(f) and not isinstance(f, type):
                    method_info.append((name, doc))
                else:
                    attributes_info.append((name, doc))
    return (method_info, attributes_info, getsizeof(obj))