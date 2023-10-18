def to_interval_values(self):
        '''Extract observation data in a `mir_eval`-friendly format.

        Returns
        -------
        intervals : np.ndarray [shape=(n, 2), dtype=float]
            Start- and end-times of all valued intervals

            `intervals[i, :] = [time[i], time[i] + duration[i]]`

        labels : list
            List view of value field.
        '''

        ints, vals = [], []
        for obs in self.data:
            ints.append([obs.time, obs.time + obs.duration])
            vals.append(obs.value)

        if not ints:
            return np.empty(shape=(0, 2), dtype=float), []

        return np.array(ints), vals