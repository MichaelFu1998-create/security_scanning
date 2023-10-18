def _make_user_class(session, name):
    """Make an Octave class for a given class name"""
    attrs = session.eval('fieldnames(%s);' % name, nout=1).ravel().tolist()
    methods = session.eval('methods(%s);' % name, nout=1).ravel().tolist()
    ref = weakref.ref(session)

    doc = _DocDescriptor(ref, name)
    values = dict(__doc__=doc, _name=name, _ref=ref, _attrs=attrs,
                  __module__='oct2py.dynamic')

    for method in methods:
        doc = _MethodDocDescriptor(ref, name, method)
        cls_name = '%s_%s' % (name, method)
        method_values = dict(__doc__=doc)
        method_cls = type(str(cls_name),
                          (OctaveUserClassMethod,), method_values)
        values[method] = method_cls(ref, method, name)

    for attr in attrs:
        values[attr] = OctaveUserClassAttr(ref, attr, attr)

    return type(str(name), (OctaveUserClass,), values)