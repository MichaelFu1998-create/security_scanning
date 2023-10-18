def _make_signature_key(args, kwargs):
    """
    Transforms function args into a key that can be used by the cache

    CommandLine:
        xdoctest -m ubelt.util_memoize _make_signature_key

    Example:
        >>> args = (4, [1, 2])
        >>> kwargs = {'a': 'b'}
        >>> key = _make_signature_key(args, kwargs)
        >>> print('key = {!r}'.format(key))
        >>> # Some mutable types cannot be handled by ub.hash_data
        >>> import pytest
        >>> import six
        >>> if six.PY2:
        >>>     import collections as abc
        >>> else:
        >>>     from collections import abc
        >>> with pytest.raises(TypeError):
        >>>     _make_signature_key((4, [1, 2], {1: 2, 'a': 'b'}), kwargs={})
        >>> class Dummy(abc.MutableSet):
        >>>     def __contains__(self, item): return None
        >>>     def __iter__(self): return iter([])
        >>>     def __len__(self): return 0
        >>>     def add(self, item, loc): return None
        >>>     def discard(self, item): return None
        >>> with pytest.raises(TypeError):
        >>>     _make_signature_key((Dummy(),), kwargs={})
    """
    kwitems = kwargs.items()
    # TODO: we should check if Python is at least 3.7 and sort by kwargs
    # keys otherwise. Should we use hash_data for key generation
    if (sys.version_info.major, sys.version_info.minor) < (3, 7):  # nocover
        # We can sort because they keys are gaurenteed to be strings
        kwitems = sorted(kwitems)
    kwitems = tuple(kwitems)

    try:
        key = _hashable(args), _hashable(kwitems)
    except TypeError:
        raise TypeError('Signature is not hashable: args={} kwargs{}'.format(args, kwargs))
    return key