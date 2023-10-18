def _format_call(call, args):
    """
    Return `call` formatted appropriately for `args`.

    :param call: A pyconfig call object
    :param args: Arguments from the command
    :type call: :class:`_PyconfigCall`

    """
    out = ''
    if args.source:
        out += call.annotation() + '\n'

    if args.only_keys:
        out += call.get_key()
        return out

    if args.view_call:
        out += call.as_call()
    elif args.load_configs:
        out += call.as_live()
    else:
        out += call.as_namespace()

    return out