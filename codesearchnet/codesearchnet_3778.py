def string_to_dict(var_string, allow_kv=True, require_dict=True):
    """Returns a dictionary given a string with yaml or json syntax.
    If data is not present in a key: value format, then it return
    an empty dictionary.

    Attempts processing string by 3 different methods in order:
        1. as JSON      2. as YAML      3. as custom key=value syntax
    Throws an error if all of these fail in the standard ways."""
    # try:
    #     # Accept all valid "key":value types of json
    #     return_dict = json.loads(var_string)
    #     assert type(return_dict) is dict
    # except (TypeError, AttributeError, ValueError, AssertionError):
    try:
        # Accept all JSON and YAML
        return_dict = yaml.load(var_string, Loader=yaml.SafeLoader)
        if require_dict:
            assert type(return_dict) is dict
    except (AttributeError, yaml.YAMLError, AssertionError):
        # if these fail, parse by key=value syntax
        try:
            assert allow_kv
            return_dict = parse_kv(var_string)
        except Exception:
            raise exc.TowerCLIError(
                'failed to parse some of the extra '
                'variables.\nvariables: \n%s' % var_string
            )
    return return_dict