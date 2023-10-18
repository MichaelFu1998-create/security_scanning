def mean(self, axis=None, dtype=None, out=None, keepdims=False):
        """Compute the arithmetic mean along the specified axis.
        See np.mean() for details."""
        if axis == -1:
            axis = self.ndim
        if axis is None:
            results = vectorize(mean)(self, axis, dtype, keepdims=False)
            weights = self._sublengths
            res = np.average(results, axis=None, weights=weights)
            if keepdims:
                for i in range(self.ndim):
                    res = expand_dims(res, res.ndim)
        elif axis == self._distaxis:
            results = vectorize(mean)(self, axis, dtype, keepdims=True)
            results = gather(results)
            # Average manually (np.average doesn't preserve ndarray subclasses)
            weights = (np.array(self._sublengths, dtype=np.float64) /
                       sum(self._sublengths))
            ix = [slice(None)] * self.ndim
            ix[axis] = 0
            res = results[ix] * weights[0]
            for i in range(1, self._n):
                ix[axis] = i
                res = res + results[ix] * weights[i]
            if keepdims:
                res = expand_dims(res, axis)
        else:
            res = vectorize(mean)(self, axis, dtype, keepdims=False)
            if keepdims:
                res = expand_dims(res, axis)
        if out is not None:
            out[:] = res
        return res