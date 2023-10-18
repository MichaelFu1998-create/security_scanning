def _register_builtin_class_extensions(self):
        """
        Register hashing extensions for a selection of classes included in
        python stdlib.

        Example:
            >>> data = uuid.UUID('7e9d206b-dc02-4240-8bdb-fffe858121d0')
            >>> print(hash_data(data, base='abc', hasher='sha512', types=True)[0:8])
            cryarepd
            >>> data = OrderedDict([('a', 1), ('b', 2), ('c', [1, 2, 3]),
            >>>                     (4, OrderedDict())])
            >>> print(hash_data(data, base='abc', hasher='sha512', types=True)[0:8])
            qjspicvv

            gpxtclct
        """
        @self.register(uuid.UUID)
        def _hash_uuid(data):
            hashable = data.bytes
            prefix = b'UUID'
            return prefix, hashable

        @self.register(OrderedDict)
        def _hash_ordered_dict(data):
            """
            Note, we should not be hashing dicts because they are unordered
            """
            hashable = b''.join(_hashable_sequence(list(data.items())))
            prefix = b'ODICT'
            return prefix, hashable