def set_verbosity(self, verbosity='vvv', handlers=None):
        """
        Set the verbosity level of a certain log handler or of all handlers.

        Parameters
        ----------
        verbosity : 'v' to 'vvvvv'
            the level of verbosity, more v's is more verbose

        handlers : string, or list of strings
            handler names can be found in ``peri.logger.types.keys()``
            Current set is::

                ['console-bw', 'console-color', 'rotating-log']
        """
        self.verbosity = sanitize(verbosity)
        self.set_level(v2l[verbosity], handlers=handlers)
        self.set_formatter(v2f[verbosity], handlers=handlers)