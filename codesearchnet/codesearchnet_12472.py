def maybe_replace_any_if_equal(name, expected, actual):
    """Return the type given in `expected`.

    Raise ValueError if `expected` isn't equal to `actual`.  If --replace-any is
    used, the Any type in `actual` is considered equal.

    The implementation is naively checking if the string representation of
    `actual` is one of "Any", "typing.Any", or "t.Any".  This is done for two
    reasons:

    1. I'm lazy.
    2. We want people to be able to explicitly state that they want Any without it
       being replaced.  This way they can use an alias.
    """
    is_equal = expected == actual
    if not is_equal and Config.replace_any:
        actual_str = minimize_whitespace(str(actual))
        if actual_str and actual_str[0] in {'"', "'"}:
            actual_str = actual_str[1:-1]
        is_equal = actual_str in {'Any', 'typing.Any', 't.Any'}

    if not is_equal:
        expected_annotation = minimize_whitespace(str(expected))
        actual_annotation = minimize_whitespace(str(actual))
        raise ValueError(
            f"incompatible existing {name}. " +
            f"Expected: {expected_annotation!r}, actual: {actual_annotation!r}"
        )

    return expected or actual