def ifetch_single(iterable, key, default=EMPTY, getter=None):
    """
    getter() g(item, key):pass
    """

    def _getter(item):
        if getter:
            custom_getter = partial(getter, key=key)
            return custom_getter(item)
        else:
            try:
                attrgetter = operator.attrgetter(key)
                return attrgetter(item)
            except AttributeError:
                pass

            try:
                itemgetter = operator.itemgetter(key)
                return itemgetter(item)
            except KeyError:
                pass

            if default is not EMPTY:
                return default

            raise ValueError('Item %r has no attr or key for %r' % (item, key))

    return map(_getter, iterable)