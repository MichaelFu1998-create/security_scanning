def transform(self, jam):
        '''Iterative transformation generator

        Applies the deformation to an input jams object.

        This generates a sequence of deformed output JAMS.

        Parameters
        ----------
        jam : jams.JAMS
            The jam to transform

        Examples
        --------
        >>> for jam_out in deformer.transform(jam_in):
        ...     process(jam_out)
        '''

        for state in self.states(jam):
            yield self._transform(jam, state)