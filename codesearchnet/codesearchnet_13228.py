def append_columns(self, columns):
        '''Add observations from column-major storage.

        This is primarily used for deserializing densely packed data.

        Parameters
        ----------
        columns : dict of lists
            Keys must be `time, duration, value, confidence`,
            and each much be a list of equal length.

        '''
        self.append_records([dict(time=t, duration=d, value=v, confidence=c)
                             for (t, d, v, c)
                             in six.moves.zip(columns['time'],
                                              columns['duration'],
                                              columns['value'],
                                              columns['confidence'])])