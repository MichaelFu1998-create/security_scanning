def signature(dbus_object, unpack=False):
    """
    Get the signature of a dbus object.

    :param dbus_object: the object
    :type dbus_object: a dbus object
    :param bool unpack: if True, unpack from enclosing variant type
    :returns: the corresponding signature
    :rtype: str
    """
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches

    if dbus_object.variant_level != 0 and not unpack:
        return 'v'

    if isinstance(dbus_object, dbus.Array):
        sigs = frozenset(signature(x) for x in dbus_object)
        len_sigs = len(sigs)
        if len_sigs > 1:  # pragma: no cover
            raise IntoDPValueError(dbus_object, "dbus_object",
                                   "has bad signature")

        if len_sigs == 0:
            return 'a' + dbus_object.signature

        return 'a' + [x for x in sigs][0]

    if isinstance(dbus_object, dbus.Struct):
        sigs = (signature(x) for x in dbus_object)
        return '(' + "".join(x for x in sigs) + ')'

    if isinstance(dbus_object, dbus.Dictionary):
        key_sigs = frozenset(signature(x) for x in dbus_object.keys())
        value_sigs = frozenset(signature(x) for x in dbus_object.values())

        len_key_sigs = len(key_sigs)
        len_value_sigs = len(value_sigs)

        if len_key_sigs != len_value_sigs:  # pragma: no cover
            raise IntoDPValueError(dbus_object, "dbus_object",
                                   "has bad signature")

        if len_key_sigs > 1:  # pragma: no cover
            raise IntoDPValueError(dbus_object, "dbus_object",
                                   "has bad signature")

        if len_key_sigs == 0:
            return 'a{' + dbus_object.signature + '}'

        return 'a{' + [x for x in key_sigs][0] + [x
                                                  for x in value_sigs][0] + '}'

    if isinstance(dbus_object, dbus.Boolean):
        return 'b'

    if isinstance(dbus_object, dbus.Byte):
        return 'y'

    if isinstance(dbus_object, dbus.Double):
        return 'd'

    if isinstance(dbus_object, dbus.Int16):
        return 'n'

    if isinstance(dbus_object, dbus.Int32):
        return 'i'

    if isinstance(dbus_object, dbus.Int64):
        return 'x'

    if isinstance(dbus_object, dbus.ObjectPath):
        return 'o'

    if isinstance(dbus_object, dbus.Signature):
        return 'g'

    if isinstance(dbus_object, dbus.String):
        return 's'

    if isinstance(dbus_object, dbus.UInt16):
        return 'q'

    if isinstance(dbus_object, dbus.UInt32):
        return 'u'

    if isinstance(dbus_object, dbus.UInt64):
        return 't'

    if isinstance(dbus_object, dbus.types.UnixFd):  # pragma: no cover
        return 'h'

    raise IntoDPValueError(dbus_object, "dbus_object",
                           "has no signature")