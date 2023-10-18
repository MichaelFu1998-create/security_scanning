def append_records(self, records):
        '''Add observations from row-major storage.

        This is primarily useful for deserializing sparsely packed data.

        Parameters
        ----------
        records : iterable of dicts or Observations
            Each element of `records` corresponds to one observation.
        '''
        for obs in records:
            if isinstance(obs, Observation):
                self.append(**obs._asdict())
            else:
                self.append(**obs)