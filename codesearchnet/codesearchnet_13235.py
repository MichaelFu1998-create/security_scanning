def to_samples(self, times, confidence=False):
        '''Sample the annotation at specified times.

        Parameters
        ----------
        times : np.ndarray, non-negative, ndim=1
            The times (in seconds) to sample the annotation

        confidence : bool
            If `True`, return both values and confidences.
            If `False` (default) only return values.

        Returns
        -------
        values : list
            `values[i]` is a list of observation values for intervals
            that cover `times[i]`.

        confidence : list (optional)
            `confidence` values corresponding to `values`
        '''
        times = np.asarray(times)
        if times.ndim != 1 or np.any(times < 0):
            raise ParameterError('times must be 1-dimensional and non-negative')

        idx = np.argsort(times)
        samples = times[idx]

        values = [list() for _ in samples]
        confidences = [list() for _ in samples]

        for obs in self.data:
            start = np.searchsorted(samples, obs.time)
            end = np.searchsorted(samples, obs.time + obs.duration, side='right')
            for i in range(start, end):
                values[idx[i]].append(obs.value)
                confidences[idx[i]].append(obs.confidence)

        if confidence:
            return values, confidences
        else:
            return values