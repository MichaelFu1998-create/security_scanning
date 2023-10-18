def pull(self, var, timeout=None, verbose=True):
        """
        Retrieve a value or values from the Octave session.

        Parameters
        ----------
        var : str or list
            Name of the variable(s) to retrieve.
        timeout : float, optional.
            Time to wait for response from Octave (per line).
        **kwargs: Deprecated kwargs, ignored.

        Returns
        -------
        out : object
            Object returned by Octave.

        Raises
        ------
        Oct2PyError
            If the variable does not exist in the Octave session.

        Examples
        --------
          >>> from oct2py import octave
          >>> y = [1, 2]
          >>> octave.push('y', y)
          >>> octave.pull('y')
          array([[ 1.,  2.]])
          >>> octave.push(['x', 'y'], ['spam', [1, 2, 3, 4]])
          >>> octave.pull(['x', 'y'])  # doctest: +SKIP
          [u'spam', array([[1, 2, 3, 4]])]

        """
        if isinstance(var, (str, unicode)):
            var = [var]
        outputs = []
        for name in var:
            exist = self._exist(name)
            if exist == 1:
                outputs.append(self.feval('evalin', 'base', name,
                                          timeout=timeout, verbose=verbose))
            else:
                outputs.append(self.get_pointer(name, timeout=timeout))

        if len(outputs) == 1:
            return outputs[0]
        return outputs