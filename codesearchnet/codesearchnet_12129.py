def default(self, obj):
        '''Overrides the default serializer for `JSONEncoder`.

        This can serialize the following objects in addition to what
        `JSONEncoder` can already do.

        - `np.array`
        - `bytes`
        - `complex`
        - `np.float64` and other `np.dtype` objects

        Parameters
        ----------

        obj : object
            A Python object to serialize to JSON.

        Returns
        -------

        str
            A JSON encoded representation of the input object.

        '''

        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return obj.decode()
        elif isinstance(obj, complex):
            return (obj.real, obj.imag)
        elif (isinstance(obj, (float, np.float64, np.float_)) and
              not np.isfinite(obj)):
            return None
        elif isinstance(obj, (np.int8, np.int16, np.int32, np.int64)):
            return int(obj)
        else:
            return json.JSONEncoder.default(self, obj)