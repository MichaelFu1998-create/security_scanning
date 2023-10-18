def with_prefix(self, prefix, strict=False):
        """
            decorator to handle commands with prefixes

        Parameters
        ----------
        prefix : str
            the prefix of the command
        strict : bool, optional
            If set to True the command must be at the beginning
            of the message. Defaults to False.

        Returns
        -------
        function
            a decorator that returns an :class:`EventHandler` instance
        """

        def decorated(func):
            return EventHandler(func=func, event=self.event,
                                prefix=prefix, strict=strict)

        return decorated