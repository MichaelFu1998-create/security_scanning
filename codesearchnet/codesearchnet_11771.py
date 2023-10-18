def create_module(name, code=None):
    """
    Dynamically creates a module with the given name.
    """

    if name not in sys.modules:
        sys.modules[name] = imp.new_module(name)

    module = sys.modules[name]

    if code:
        print('executing code for %s: %s' % (name, code))
        exec(code in module.__dict__) # pylint: disable=exec-used
        exec("from %s import %s" % (name, '*')) # pylint: disable=exec-used

    return module