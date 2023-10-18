def _handle_module(args):
    """
    Handles the -m argument.

    """
    module = _get_module_filename(args.module)
    if not module:
        _error("Could not load module or package: %r", args.module)
    elif isinstance(module, Unparseable):
        _error("Could not determine module source: %r", args.module)

    _parse_and_output(module, args)