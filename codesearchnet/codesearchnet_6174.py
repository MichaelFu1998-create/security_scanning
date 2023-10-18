def dynamic_instantiate_middleware(name, args, expand=None):
    """Import a class and instantiate with custom args.

    Example:
        name = "my.module.Foo"
        args_dict = {
            "bar": 42,
            "baz": "qux"
            }
        =>
        from my.module import Foo
        return Foo(bar=42, baz="qux")
    """

    def _expand(v):
        """Replace some string templates with defined values."""
        if expand and compat.is_basestring(v) and v.lower() in expand:
            return expand[v]
        return v

    try:
        the_class = dynamic_import_class(name)
        inst = None
        if type(args) in (tuple, list):
            args = tuple(map(_expand, args))
            inst = the_class(*args)
        else:
            assert type(args) is dict
            args = {k: _expand(v) for k, v in args.items()}
            inst = the_class(**args)

        _logger.debug("Instantiate {}({}) => {}".format(name, args, inst))
    except Exception:
        _logger.exception("ERROR: Instantiate {}({}) => {}".format(name, args, inst))

    return inst