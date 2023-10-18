def unpack_from_dict(fmt, names, data, offset=0):
    """Same as :func:`~bitstruct.unpack_from_dict()`, but returns a
    dictionary.

    See :func:`~bitstruct.pack_dict()` for details on `names`.

    """

    return CompiledFormatDict(fmt, names).unpack_from(data, offset)