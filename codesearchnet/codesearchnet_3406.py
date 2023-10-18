def decree(cls, path, concrete_start='', **kwargs):
        """
        Constructor for Decree binary analysis.

        :param str path: Path to binary to analyze
        :param str concrete_start: Concrete stdin to use before symbolic input
        :param kwargs: Forwarded to the Manticore constructor
        :return: Manticore instance, initialized with a Decree State
        :rtype: Manticore
        """
        try:
            return cls(_make_decree(path, concrete_start), **kwargs)
        except KeyError:  # FIXME(mark) magic parsing for DECREE should raise better error
            raise Exception(f'Invalid binary: {path}')