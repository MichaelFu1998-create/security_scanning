def validate_litezip(struct):
    """Validate the given litezip as `struct`.
    Returns a list of validation messages.

    """
    msgs = []

    def _fmt_err(err):
        return (Path(err.filename), "{}:{} -- {}: {}".format(*(err[1:])))

    obj_by_type = {}
    for obj in struct:
        if not is_valid_identifier(obj.id):
            msg = (obj.file.parent,
                   "{} is not a valid identifier".format(obj.id),)
            logger.info("{}: {}".format(*msg))
            msgs.append(msg)
        obj_by_type.setdefault(type(obj), []).append(obj)

    for obtype in obj_by_type:
        content_msgs = list([_fmt_err(err) for err in
                             validate_content(*obj_by_type[obtype])])
        for msg in content_msgs:
            logger.info("{}: {}".format(*msg))
        msgs.extend(content_msgs)
    return msgs