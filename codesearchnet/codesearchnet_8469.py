def rehome(old, new, struct):
    """
    Replace all absolute paths to "re-home" it
    """

    if old == new:
        return

    if isinstance(struct, list):
        for item in struct:
            rehome(old, new, item)
    elif isinstance(struct, dict):
        for key, val in struct.iteritems():
            if isinstance(val, (dict, list)):
                rehome(old, new, val)
            elif "conf" in key:
                continue
            elif "orig" in key:
                continue
            elif "root" in key or "path" in key:
                struct[key] = struct[key].replace(old, new)