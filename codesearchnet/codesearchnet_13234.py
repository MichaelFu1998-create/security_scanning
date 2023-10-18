def to_event_values(self):
        '''Extract observation data in a `mir_eval`-friendly format.

        Returns
        -------
        times : np.ndarray [shape=(n,), dtype=float]
            Start-time of all observations

        labels : list
            List view of value field.
        '''
        ints, vals = [], []
        for obs in self.data:
            ints.append(obs.time)
            vals.append(obs.value)

        return np.array(ints), vals