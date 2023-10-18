def json_get_default(json: JsonValue, path: str,
                     default: Any, expected_type: Any = ANY) -> Any:
    """Get a JSON value by path, optionally checking its type.

    This works exactly like json_get(), but instead of raising
    ValueError or IndexError when a path part is not found, return
    the provided default value:

    >>> json_get_default({}, "/foo", "I am a default value")
    'I am a default value'

    TypeErrors will be raised as in json_get() if an expected_type
    is provided:

    >>> json_get_default({"foo": "bar"}, "/foo", 123, int)
    Traceback (most recent call last):
        ...
    TypeError: wrong JSON type int != str
    """
    try:
        return json_get(json, path, expected_type)
    except (ValueError, IndexError):
        return default