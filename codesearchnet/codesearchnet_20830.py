def are_connected(self, body_a, body_b):
        '''Determine whether the given bodies are currently connected.

        Parameters
        ----------
        body_a : str or :class:`Body`
            One body to test for connectedness. If this is a string, it is
            treated as the name of a body to look up.
        body_b : str or :class:`Body`
            One body to test for connectedness. If this is a string, it is
            treated as the name of a body to look up.

        Returns
        -------
        connected : bool
            Return True iff the two bodies are connected.
        '''
        return bool(ode.areConnected(
            self.get_body(body_a).ode_body,
            self.get_body(body_b).ode_body))