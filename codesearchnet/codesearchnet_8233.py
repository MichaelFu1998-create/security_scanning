def make_object(*args, typename=None, python_path=None, datatype=None, **kwds):
    """Make an object from a symbol."""
    datatype = datatype or import_symbol(typename, python_path)
    field_types = getattr(datatype, 'FIELD_TYPES', fields.FIELD_TYPES)
    return datatype(*args, **fields.component(kwds, field_types))