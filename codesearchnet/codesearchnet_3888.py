def register(self, hash_types):
        """
        Registers a function to generate a hash for data of the appropriate
        types. This can be used to register custom classes. Internally this is
        used to define how to hash non-builtin objects like ndarrays and uuids.

        The registered function should return a tuple of bytes. First a small
        prefix hinting at the data type, and second the raw bytes that can be
        hashed.

        Args:
            hash_types (class or tuple of classes):

        Returns:
            func: closure to be used as the decorator

        Example:
            >>> # xdoctest: +SKIP
            >>> # Skip this doctest because we dont want tests to modify
            >>> # the global state.
            >>> import ubelt as ub
            >>> import pytest
            >>> class MyType(object):
            ...     def __init__(self, id):
            ...         self.id = id
            >>> data = MyType(1)
            >>> # Custom types wont work with ub.hash_data by default
            >>> with pytest.raises(TypeError):
            ...     ub.hash_data(data)
            >>> # You can register your functions with ubelt's internal
            >>> # hashable_extension registery.
            >>> @ub.util_hash._HASHABLE_EXTENSIONS.register(MyType)
            >>> def hash_my_type(data):
            ...     return b'mytype', six.b(ub.hash_data(data.id))
            >>> # TODO: allow hash_data to take an new instance of
            >>> # HashableExtensions, so we dont have to modify the global
            >>> # ubelt state when we run tests.
            >>> my_instance = MyType(1)
            >>> ub.hash_data(my_instance)
        """
        # ensure iterable
        if not isinstance(hash_types, (list, tuple)):
            hash_types = [hash_types]
        def _decor_closure(hash_func):
            for hash_type in hash_types:
                key = (hash_type.__module__, hash_type.__name__)
                self.keyed_extensions[key] = (hash_type, hash_func)
            return hash_func
        return _decor_closure