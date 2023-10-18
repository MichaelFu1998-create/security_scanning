def _prompt_for_values(d):
    """Update the descriptive metadata interactively.

    Uses values entered by the user. Note that the function keeps recursing
    whenever a value is another ``CommentedMap`` or a ``list``. The
    function works as passing dictionaries and lists into a function edits
    the values in place.
    """
    for key, value in d.items():
        if isinstance(value, CommentedMap):
            _prompt_for_values(value)
        elif isinstance(value, list):
            for item in value:
                _prompt_for_values(item)
        else:
            typ = type(value)

            if isinstance(value, ScalarFloat):  # Deal with ruamel.yaml floats.
                typ = float

            new_value = click.prompt(key, type=typ, default=value)
            d[key] = new_value
    return d