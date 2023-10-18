def pack_into_dict(fmt, names, buf, offset, data, **kwargs):
    """Same as :func:`~bitstruct.pack_into()`, but data is read from a
    dictionary.

    See :func:`~bitstruct.pack_dict()` for details on `names`.

    """

    return CompiledFormatDict(fmt, names).pack_into(buf,
                                                    offset,
                                                    data,
                                                    **kwargs)