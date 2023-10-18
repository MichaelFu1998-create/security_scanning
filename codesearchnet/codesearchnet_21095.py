def json_get(json: JsonValue, path: str, expected_type: Any = ANY) -> Any:
    """Get a JSON value by path, optionally checking its type.

    >>> j = {"foo": {"num": 3.4, "s": "Text"}, "arr": [10, 20, 30]}
    >>> json_get(j, "/foo/num")
    3.4
    >>> json_get(j, "/arr[1]")
    20

    Raise ValueError if the path is not found:

    >>> json_get(j, "/foo/unknown")
    Traceback (most recent call last):
        ...
    ValueError: JSON path '/foo/unknown' not found

    Raise TypeError if the path contains a non-object element:

    >>> json_get(j, "/foo/num/bar")
    Traceback (most recent call last):
        ...
    TypeError: JSON path '/foo/num' is not an object

    Or a non-array element:

    >>> json_get(j, "/foo[2]")
    Traceback (most recent call last):
        ...
    TypeError: JSON path '/foo' is not an array

    Raise an IndexError if the array index is out of bounds:

    >>> json_get(j, "/arr[10]")
    Traceback (most recent call last):
        ...
    IndexError: JSON array '/arr' too small (3 <= 10)

    Recognized types are: str, int, float, bool, list, dict, and None.
    TypeError is raised if the type does not match.

    >>> json_get(j, "/foo/num", str)
    Traceback (most recent call last):
        ...
    TypeError: wrong JSON type str != float

    float will match any number, int will only match numbers without a
    fractional part.

    >>> json_get(j, "/foo/num", float)
    3.4
    >>> json_get(j, "/foo/num", int)
    Traceback (most recent call last):
        ...
    TypeError: wrong JSON type int != float
    """

    elements = _parse_json_path(path)

    current = json
    current_path = ""
    for i, element in enumerate(elements):
        if isinstance(element, str):
            if not isinstance(current, dict):
                msg = "JSON path '{}' is not an object".format(current_path)
                raise TypeError(msg) from None
            if element not in current:
                raise ValueError("JSON path '{}' not found".format(path))
            current_path += "/" + element
            current = current[element]
        else:
            if not isinstance(current, list):
                msg = "JSON path '{}' is not an array".format(current_path)
                raise TypeError(msg) from None
            if element >= len(current):
                msg = "JSON array '{}' too small ({} <= {})".format(
                    current_path, len(current), element)
                raise IndexError(msg)
            current_path += "[{}]".format(i)
            current = current[element]
    if expected_type != ANY:
        assert_json_type(current, cast(JsonType, expected_type))
    return current