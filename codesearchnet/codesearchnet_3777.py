def parse_kv(var_string):
    """Similar to the Ansible function of the same name, parses file
    with a key=value pattern and stores information in a dictionary,
    but not as fully featured as the corresponding Ansible code."""
    return_dict = {}

    # Output updates dictionaries, so return empty one if no vals in
    if var_string is None:
        return {}

    # Python 2.6 / shlex has problems handling unicode, this is a fix
    fix_encoding_26 = False
    if sys.version_info < (2, 7) and '\x00' in shlex.split(u'a')[0]:
        fix_encoding_26 = True

    # Also hedge against Click library giving non-string type
    is_unicode = False
    if fix_encoding_26 or not isinstance(var_string, str):
        if isinstance(var_string, six.text_type):
            var_string = var_string.encode('UTF-8')
            is_unicode = True
        else:
            var_string = str(var_string)

    # Use shlex library to split string by quotes, whitespace, etc.
    for token in shlex.split(var_string):

        # Second part of fix to avoid passing shlex unicode in py2.6
        if (is_unicode):
            token = token.decode('UTF-8')
        if fix_encoding_26:
            token = six.text_type(token)
        # Look for key=value pattern, if not, process as raw parameter
        if '=' in token:
            (k, v) = token.split('=', 1)
            # If '=' are unbalanced, then stop and warn user
            if len(k) == 0 or len(v) == 0:
                raise Exception
            # If possible, convert into python data type, for instance "5"->5
            try:
                return_dict[k] = ast.literal_eval(v)
            except Exception:
                return_dict[k] = v
        else:
            # scenario where --extra-vars=42, will throw error
            raise Exception

    return return_dict