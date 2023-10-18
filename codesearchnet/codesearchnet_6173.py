def dynamic_import_class(name):
    """Import a class from a module string, e.g. ``my.module.ClassName``."""
    import importlib

    module_name, class_name = name.rsplit(".", 1)
    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        _logger.exception("Dynamic import of {!r} failed: {}".format(name, e))
        raise
    the_class = getattr(module, class_name)
    return the_class