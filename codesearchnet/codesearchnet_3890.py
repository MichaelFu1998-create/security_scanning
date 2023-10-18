def _register_numpy_extensions(self):
        """
        Numpy extensions are builtin
        """
        # system checks
        import numpy as np
        numpy_floating_types = (np.float16, np.float32, np.float64)
        if hasattr(np, 'float128'):  # nocover
            numpy_floating_types = numpy_floating_types + (np.float128,)

        @self.add_iterable_check
        def is_object_ndarray(data):
            # ndarrays of objects cannot be hashed directly.
            return isinstance(data, np.ndarray) and data.dtype.kind == 'O'

        @self.register(np.ndarray)
        def hash_numpy_array(data):
            """
            Example:
                >>> import ubelt as ub
                >>> if not ub.modname_to_modpath('numpy'):
                ...     raise pytest.skip()
                >>> import numpy as np
                >>> data_f32 = np.zeros((3, 3, 3), dtype=np.float64)
                >>> data_i64 = np.zeros((3, 3, 3), dtype=np.int64)
                >>> data_i32 = np.zeros((3, 3, 3), dtype=np.int32)
                >>> hash_f64 = _hashable_sequence(data_f32, types=True)
                >>> hash_i64 = _hashable_sequence(data_i64, types=True)
                >>> hash_i32 = _hashable_sequence(data_i64, types=True)
                >>> assert hash_i64 != hash_f64
                >>> assert hash_i64 != hash_i32
            """
            if data.dtype.kind == 'O':
                msg = 'directly hashing ndarrays with dtype=object is unstable'
                raise TypeError(msg)
            else:
                # tobytes() views the array in 1D (via ravel())
                # encode the shape as well
                header = b''.join(_hashable_sequence((len(data.shape), data.shape)))
                dtype = b''.join(_hashable_sequence(data.dtype.descr))
                hashable = header + dtype + data.tobytes()
            prefix = b'NDARR'
            return prefix, hashable

        @self.register((np.int64, np.int32, np.int16, np.int8) +
                       (np.uint64, np.uint32, np.uint16, np.uint8))
        def _hash_numpy_int(data):
            return _convert_to_hashable(int(data))

        @self.register(numpy_floating_types)
        def _hash_numpy_float(data):
            return _convert_to_hashable(float(data))

        @self.register(np.random.RandomState)
        def _hash_numpy_random_state(data):
            """
            Example:
                >>> import ubelt as ub
                >>> if not ub.modname_to_modpath('numpy'):
                ...     raise pytest.skip()
                >>> import numpy as np
                >>> rng = np.random.RandomState(0)
                >>> _hashable_sequence(rng, types=True)
            """
            hashable = b''.join(_hashable_sequence(data.get_state()))
            prefix = b'RNG'
            return prefix, hashable