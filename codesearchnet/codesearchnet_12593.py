def _unpackb3(s, **options):
    """
    Deserialize MessagePack bytes into a Python object.

    Args:
        s: a 'bytes' or 'bytearray' containing serialized MessagePack bytes

    Kwargs:
        ext_handlers (dict): dictionary of Ext handlers, mapping integer Ext
                             type to a callable that unpacks an instance of
                             Ext into an object
        use_ordered_dict (bool): unpack maps into OrderedDict, instead of
                                 unordered dict (default False)
        allow_invalid_utf8 (bool): unpack invalid strings into instances of
                                   InvalidString, for access to the bytes
                                   (default False)

    Returns:
        A Python object.

    Raises:
        TypeError:
            Packed data type is neither 'bytes' nor 'bytearray'.
        InsufficientDataException(UnpackException):
            Insufficient data to unpack the serialized object.
        InvalidStringException(UnpackException):
            Invalid UTF-8 string encountered during unpacking.
        UnsupportedTimestampException(UnpackException):
            Unsupported timestamp format encountered during unpacking.
        ReservedCodeException(UnpackException):
            Reserved code encountered during unpacking.
        UnhashableKeyException(UnpackException):
            Unhashable key encountered during map unpacking.
            The serialized map cannot be deserialized into a Python dictionary.
        DuplicateKeyException(UnpackException):
            Duplicate key encountered during map unpacking.

    Example:
    >>> umsgpack.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00')
    {'compact': True, 'schema': 0}
    >>>
    """
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError("packed data must be type 'bytes' or 'bytearray'")
    return _unpack(io.BytesIO(s), options)