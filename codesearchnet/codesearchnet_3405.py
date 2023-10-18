def linux(cls, path, argv=None, envp=None, entry_symbol=None, symbolic_files=None, concrete_start='', pure_symbolic=False, stdin_size=None, **kwargs):
        """
        Constructor for Linux binary analysis.

        :param str path: Path to binary to analyze
        :param argv: Arguments to provide to the binary
        :type argv: list[str]
        :param envp: Environment to provide to the binary
        :type envp: dict[str, str]
        :param entry_symbol: Entry symbol to resolve to start execution
        :type envp: str
        :param symbolic_files: Filenames to mark as having symbolic input
        :type symbolic_files: list[str]
        :param str concrete_start: Concrete stdin to use before symbolic input
        :param int stdin_size: symbolic stdin size to use
        :param kwargs: Forwarded to the Manticore constructor
        :return: Manticore instance, initialized with a Linux State
        :rtype: Manticore
        """
        if stdin_size is None:
            stdin_size = consts.stdin_size

        try:
            return cls(_make_linux(path, argv, envp, entry_symbol, symbolic_files, concrete_start, pure_symbolic, stdin_size), **kwargs)
        except elftools.common.exceptions.ELFError:
            raise Exception(f'Invalid binary: {path}')