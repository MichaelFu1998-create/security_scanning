def to_type_constructor(value, python_path=None):
    """"
    Tries to convert a value to a type constructor.

    If value is a string, then it used as the "typename" field.

    If the "typename" field exists, the symbol for that name is imported and
    added to the type constructor as a field "datatype".

    Throws:
         ImportError -- if "typename" is set but cannot be imported
         ValueError -- if "typename" is malformed
    """
    if not value:
        return value

    if callable(value):
        return {'datatype': value}

    value = to_type(value)
    typename = value.get('typename')
    if typename:
        r = aliases.resolve(typename)
        try:
            value['datatype'] = importer.import_symbol(
                r, python_path=python_path)
            del value['typename']
        except Exception as e:
            value['_exception'] = e

    return value