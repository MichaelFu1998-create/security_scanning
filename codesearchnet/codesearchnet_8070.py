def transform(self, jam):
        '''Apply the sequence of transformations to a single jam object.

        Parameters
        ----------
        jam : jams.JAMS
            The jam object to transform

        Yields
        ------
        jam_out : jams.JAMS
            The jam objects produced by the transformation sequence
        '''

        for output in self.__recursive_transform(jam, self.steps):
            yield output