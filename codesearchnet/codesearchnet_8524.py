def extracting(self, *names, **kwargs):
        """Asserts that val is collection, then extracts the named properties or named zero-arg methods into a list (or list of tuples if multiple names are given)."""
        if not isinstance(self.val, Iterable):
            raise TypeError('val is not iterable')
        if isinstance(self.val, str_types):
            raise TypeError('val must not be string')
        if len(names) == 0:
            raise ValueError('one or more name args must be given')

        def _extract(x, name):
            if self._check_dict_like(x, check_values=False, return_as_bool=True):
                if name in x:
                    return x[name]
                else:
                    raise ValueError('item keys %s did not contain key <%s>' % (list(x.keys()), name))
            elif isinstance(x, Iterable):
                self._check_iterable(x, name='item')
                return x[name]
            elif hasattr(x, name):
                attr = getattr(x, name)
                if callable(attr):
                    try:
                        return attr()
                    except TypeError:
                        raise ValueError('val method <%s()> exists, but is not zero-arg method' % name)
                else:
                    return attr
            else:
                raise ValueError('val does not have property or zero-arg method <%s>' % name)

        def _filter(x):
            if 'filter' in kwargs:
                if isinstance(kwargs['filter'], str_types):
                    return bool(_extract(x, kwargs['filter']))
                elif self._check_dict_like(kwargs['filter'], check_values=False, return_as_bool=True):
                    for k in kwargs['filter']:
                        if isinstance(k, str_types):
                            if _extract(x, k) != kwargs['filter'][k]:
                                return False
                    return True
                elif callable(kwargs['filter']):
                    return kwargs['filter'](x)
                return False
            return True

        def _sort(x):
            if 'sort' in kwargs:
                if isinstance(kwargs['sort'], str_types):
                    return _extract(x, kwargs['sort'])
                elif isinstance(kwargs['sort'], Iterable):
                    items = []
                    for k in kwargs['sort']:
                        if isinstance(k, str_types):
                            items.append(_extract(x, k))
                    return tuple(items)
                elif callable(kwargs['sort']):
                    return kwargs['sort'](x)
            return 0

        extracted = []
        for i in sorted(self.val, key=lambda x: _sort(x)):
            if _filter(i):
                items = [_extract(i, name) for name in names]
                extracted.append(tuple(items) if len(items) > 1 else items[0])
        return AssertionBuilder(extracted, self.description, self.kind)