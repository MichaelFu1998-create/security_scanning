def proxy_methods(base, include_underscore=None, exclude=None, supers=True):
    """class decorator. Modifies `Remote` subclasses to add proxy methods and
    attributes that mimic those defined in class `base`.

    Example:

      @proxy_methods(Tree)
      class RemoteTree(Remote, Tree)

    The decorator registers the new proxy class and specifies which methods
    and attributes of class `base` should be proxied via a remote call to
    a real object, and which methods/attributes should not be proxied but
    instead called directly on the instance of the proxy class.

    By default all methods and attributes of the class `base` will be
    proxied except those starting with an underscore.

    The MRO of the decorated class is respected:
    Any methods and attributes defined in the decorated class
    (or in other bases of the decorated class that do not come after `base`
     in its MRO) will override those added by this decorator,
    so that `base` is treated like a base class.

    Args:
      base (type): The class whose instances should be remotely controlled.
      include_underscore (bool or sequence of str): Should methods or
        attributes that start with an underscore be proxied anyway? If a
        sequence of names is provided then methods or attributes starting with
        an underscore will only be proxied if their names are in the sequence.
      exclude (sequence of str): Names of any methods or attributes that 
        should not be proxied.
      supers (bool): Proxy methods and attributes defined in superclasses 
        of ``base``, in addition to those defined directly in class ``base``
    """
    always_exclude = ('__new__', '__init__', '__getattribute__', '__class__',
                      '__reduce__', '__reduce_ex__')
    if isinstance(include_underscore, str):
        include_underscore = (include_underscore,)
    if isinstance(exclude, str):
        exclude = (exclude,)
    if not include_underscore:
        include_underscore = ()
    if not exclude:
        exclude = ()
    def rebuild_class(cls):
        # Identify any bases of cls that do not come after `base` in the list:
        bases_other = list(cls.__bases__)
        if bases_other[-1] is object:
            bases_other.pop()
        if base in bases_other:
            bases_other = bases_other[:bases_other.index(base)]
        if not issubclass(cls.__bases__[0], Remote):
            raise DistobTypeError('First base class must be subclass of Remote')
        if not issubclass(base, object):
            raise DistobTypeError('Only new-style classes currently supported')
        dct = cls.__dict__.copy()
        if cls.__doc__ is None or '\n' not in cls.__doc__:
            base_doc = base.__doc__
            if base_doc is None:
                base_doc = ''
            dct['__doc__'] = """Local object representing a remote %s
                  It can be used just like a %s object, but behind the scenes 
                  all requests are passed to a real %s object on a remote host.

                  """ % ((base.__name__,)*3) + base_doc
        newcls = type(cls.__name__, cls.__bases__, dct)
        newcls._include_underscore = include_underscore
        newcls._exclude = exclude
        if supers:
            proxied_classes = base.__mro__[:-1]
        else:
            proxied_classes = (base,)
        for c in proxied_classes:
            for name in c.__dict__:
                #respect MRO: proxy an attribute only if it is not overridden
                if (name not in newcls.__dict__ and
                        all(name not in b.__dict__ 
                            for c in bases_other for b in c.mro()[:-1]) and
                        name not in newcls._exclude and
                        name not in always_exclude and
                        (name[0] != '_' or 
                         newcls._include_underscore is True or
                         name in newcls._include_underscore)):
                    f = c.__dict__[name]
                    if hasattr(f, '__doc__'):
                        doc = f.__doc__
                    else:
                        doc = None
                    if callable(f) and not isinstance(f, type):
                        setattr(newcls, name, _make_proxy_method(name, doc))
                    else:
                        setattr(newcls, name, _make_proxy_property(name, doc))
        newcls.__module__ = '__main__' # cause dill to pickle it whole
        import __main__
        __main__.__dict__[newcls.__name__] = newcls # for dill..
        ObjectHub.register_proxy_type(base, newcls)
        return newcls
    return rebuild_class