def ConstField(name, value, marshal=None):
    """
    This macro can be used in several methods:

    >>> ConstField("foo", 5, UBInt8)

    This created a constant field called ``foo`` with a value of 5 and is serialized/deserialized using UBInt8.

    >>> ConstField("foo", MyStruct(my_field=1, my_other_field=2))

    This time ``foo`` is set with the ``MyStruct`` instance passed here. Notice that we don't need to pass an I/O
    argument because the value is an I/O instance by itself.

    :param name: name of the field
    :param value: the value to use as a constant
    :param marshal: a marshal instance to serialize/deserialize this field (optional if ``value`` is a marshal)
    :rtype: Field
    """
    if marshal is None:
        marshal = value
    if isinstance(marshal, Struct):
        marshal = type(marshal)
    elif not isinstance(marshal, Marshal):
        raise InstructError("don't know how to serialize const field %s value %s (consider adding a marshal argument)" %
                            (name, value))
    return OrigConstField(name, marshal, value)