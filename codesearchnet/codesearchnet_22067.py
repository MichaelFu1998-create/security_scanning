def encode(python_object, indent=None, large_object=False):
    """:returns: a JSON-representation of the object"""
    # sorted keys is easier to read; however, Python-2.7.2 does not have this feature
    kwargs = dict(indent=indent)
    if can_dumps_sort_keys():
        kwargs.update(sort_keys=True)
    try:
        if large_object:
            out = GreenletFriendlyStringIO()
            json.dump(python_object, out, **kwargs)
            return out.getvalue()
        else:
            return json.dumps(python_object, **kwargs)
    except Exception:
        logger.exception()
        raise EncodeError('Cannot encode {!r}', python_object)