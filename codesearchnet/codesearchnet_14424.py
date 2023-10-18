def _output(calls, args):
    """
    Outputs `calls`.

    :param calls: List of :class:`_PyconfigCall` instances
    :param args: :class:`~argparse.ArgumentParser` instance
    :type calls: list
    :type args: argparse.ArgumentParser

    """
    # Sort the keys appropriately
    if args.natural_sort or args.source:
        calls = sorted(calls, key=lambda c: (c.filename, c.lineno))
    else:
        calls = sorted(calls, key=lambda c: c.key)

    out = []

    # Handle displaying only the list of keys
    if args.only_keys:
        keys = set()
        for call in calls:
            if call.key in keys:
                continue
            out.append(_format_call(call, args))
            keys.add(call.key)

        out = '\n'.join(out)
        if args.color:
            out = _colorize(out)
        print(out, end=' ')

        # We're done here
        return

    # Build a list of keys which have default values available, so that we can
    # toggle between displaying only those keys with defaults and all keys
    keys = set()
    for call in calls:
        if call.default:
            keys.add(call.key)

    for call in calls:
        if not args.all and not call.default and call.key in keys:
            continue
        out.append(_format_call(call, args))

    out = '\n'.join(out)
    if args.color:
        out = _colorize(out)
    print(out, end=' ')