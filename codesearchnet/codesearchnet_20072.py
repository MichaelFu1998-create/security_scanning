def api_subclass_factory(name, docstring, remove_methods, base=SlackApi):
    """Create an API subclass with fewer methods than its base class.

    Arguments:
      name (:py:class:`str`): The name of the new class.
      docstring (:py:class:`str`): The docstring for the new class.
      remove_methods (:py:class:`dict`): The methods to remove from
        the base class's :py:attr:`API_METHODS` for the subclass. The
        key is the name of the root method (e.g. ``'auth'`` for
        ``'auth.test'``, the value is either a tuple of child method
        names (e.g. ``('test',)``) or, if all children should be
        removed, the special value :py:const:`ALL`.
      base (:py:class:`type`, optional): The base class (defaults to
        :py:class:`SlackApi`).

    Returns:
      :py:class:`type`: The new subclass.

    Raises:
      :py:class:`KeyError`: If the method wasn't in the superclass.

    """
    methods = deepcopy(base.API_METHODS)
    for parent, to_remove in remove_methods.items():
        if to_remove is ALL:
            del methods[parent]
        else:
            for method in to_remove:
                del methods[parent][method]
    return type(name, (base,), dict(API_METHODS=methods, __doc__=docstring))