def lookup(self, data):
        """
        Returns an appropriate function to hash `data` if one has been
        registered.

        Raises:
            TypeError : if data has no registered hash methods

        Example:
            >>> import ubelt as ub
            >>> import pytest
            >>> if not ub.modname_to_modpath('numpy'):
            ...     raise pytest.skip('numpy is optional')
            >>> self = HashableExtensions()
            >>> self._register_numpy_extensions()
            >>> self._register_builtin_class_extensions()

            >>> import numpy as np
            >>> data = np.array([1, 2, 3])
            >>> self.lookup(data[0])

            >>> class Foo(object):
            >>>     def __init__(f):
            >>>         f.attr = 1
            >>> data = Foo()
            >>> assert pytest.raises(TypeError, self.lookup, data)

            >>> # If ub.hash_data doesnt support your object,
            >>> # then you can register it.
            >>> @self.register(Foo)
            >>> def _hashfoo(data):
            >>>     return b'FOO', data.attr
            >>> func = self.lookup(data)
            >>> assert func(data)[1] == 1

            >>> data = uuid.uuid4()
            >>> self.lookup(data)
        """
        # Maybe try using functools.singledispatch instead?
        # First try O(1) lookup
        query_hash_type = data.__class__
        key = (query_hash_type.__module__, query_hash_type.__name__)
        try:
            hash_type, hash_func = self.keyed_extensions[key]
        except KeyError:
            raise TypeError('No registered hash func for hashable type=%r' % (
                    query_hash_type))
        return hash_func