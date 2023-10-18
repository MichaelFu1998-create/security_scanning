def pretty_print (obj, indent=False):
    """
    pretty print a JSON object
    """

    if indent:
        return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))
    else:
        return json.dumps(obj, sort_keys=True)