def to_value(cls, instance):
        """Convert to a value to send to Octave."""
        if not isinstance(instance, OctaveUserClass) or not instance._attrs:
            return dict()
        # Bootstrap a MatlabObject from scipy.io
        # From https://github.com/scipy/scipy/blob/93a0ea9e5d4aba1f661b6bb0e18f9c2d1fce436a/scipy/io/matlab/mio5.py#L435-L443
        # and https://github.com/scipy/scipy/blob/93a0ea9e5d4aba1f661b6bb0e18f9c2d1fce436a/scipy/io/matlab/mio5_params.py#L224
        dtype = []
        values = []
        for attr in instance._attrs:
            dtype.append((str(attr), object))
            values.append(getattr(instance, attr))
        struct = np.array([tuple(values)], dtype)
        return MatlabObject(struct, instance._name)