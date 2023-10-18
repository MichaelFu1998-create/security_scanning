def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except:
            return None

    try:
        fn = inspect.getsourcefile(obj)
    except:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    fn = relpath(fn, start=dirname(scisalt.__file__))

    if 'dev' in scisalt.__version__:
        return "http://github.com/joelfrederico/SciSalt/blob/master/scisalt/%s%s" % (
            fn, linespec)
    else:
        return "http://github.com/joelfrederico/SciSalt/blob/v%s/scisalt/%s%s" % (
            scisalt.__version__, fn, linespec)