def pprint_jobject(obj, **kwargs):
    '''Pretty-print a jobject.

    Parameters
    ----------
    obj : jams.JObject

    kwargs
        additional parameters to `json.dumps`

    Returns
    -------
    string
        A simplified display of `obj` contents.
    '''

    obj_simple = {k: v for k, v in six.iteritems(obj.__json__) if v}

    string = json.dumps(obj_simple, **kwargs)

    # Suppress braces and quotes
    string = re.sub(r'[{}"]', '', string)

    # Kill trailing commas
    string = re.sub(r',\n', '\n', string)

    # Kill blank lines
    string = re.sub(r'^\s*$', '', string)

    return string