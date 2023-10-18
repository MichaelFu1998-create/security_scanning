def assert_json_type(value: JsonValue, expected_type: JsonCheckType) -> None:
    """Check that a value has a certain JSON type.

    Raise TypeError if the type does not match.

    Supported types: str, int, float, bool, list, dict, and None.
    float will match any number, int will only match numbers without
    fractional part.

    The special type JList(x) will match a list value where each
    item is of type x:

    >>> assert_json_type([1, 2, 3], JList(int))
    """

    def type_name(t: Union[JsonCheckType, Type[None]]) -> str:
        if t is None:
            return "None"
        if isinstance(t, JList):
            return "list"
        return t.__name__

    if expected_type is None:
        if value is None:
            return
    elif expected_type == float:
        if isinstance(value, float) or isinstance(value, int):
            return
    elif expected_type in [str, int, bool, list, dict]:
        if isinstance(value, expected_type):  # type: ignore
            return
    elif isinstance(expected_type, JList):
        if isinstance(value, list):
            for v in value:
                assert_json_type(v, expected_type.value_type)
            return
    else:
        raise TypeError("unsupported type")
    raise TypeError("wrong JSON type {} != {}".format(
        type_name(expected_type), type_name(type(value))))