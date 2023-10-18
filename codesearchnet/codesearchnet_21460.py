def make_repr(*args, **kwargs):
    """Returns __repr__ method which returns ASCII
    representaion of the object with given fields.

    Without arguments, ``make_repr`` generates a method
    which outputs all object's non-protected (non-undercored)
    arguments which are not callables.

    Accepts ``*args``, which should be a names of object's
    attributes to be included in the output::

      __repr__ = make_repr('foo', 'bar')

    If you want to generate attribute's content on the fly,
    then you should use keyword arguments and pass a callable
    of one argument::

      __repr__ = make_repr(foo=lambda obj: obj.blah + 100500)

    """

    def method(self):
        cls_name = self.__class__.__name__

        if args:
            field_names = args
        else:
            def undercored(name): return name.startswith('_')

            def is_method(name): return callable(getattr(self, name))

            def good_name(name):
                return not undercored(name) and not is_method(name)

            field_names = filter(good_name, dir(self))
            field_names = sorted(field_names)

        # on this stage, we make from field_names an
        # attribute getters
        field_getters = zip(field_names,
                            map(attrgetter, field_names))

        # now process keyword args, they must
        # contain callables of one argument
        # and callable should return a field's value
        field_getters = chain(
            field_getters,
            kwargs.items())

        fields = ((name, format_value(getter(self)))
                  for name, getter in field_getters)

        # prepare key strings
        fields = ((u'{0}='.format(name), value)
                  for name, value in fields)

        # join values with they respective keys
        fields = list(starmap(serialize_text, fields))

        beginning = u'<{cls_name} '.format(
            cls_name=cls_name,
        )
        result = serialize_list(
            beginning,
            fields)

        # append closing braket
        result += u'>'

        if ON_PYTHON2:
            # on python 2.x repr returns bytes, but on python3 - unicode strings
            result = result.encode('utf-8')

        return result

    return method