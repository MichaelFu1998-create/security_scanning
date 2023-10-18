def binary_symbols(binary):
    """
    helper method for getting all binary symbols with SANDSHREW_ prepended.
    We do this in order to provide the symbols Manticore should hook on to
    perform main analysis.

    :param binary: str for binary to instrospect.
    :rtype list: list of symbols from binary
    """

    def substr_after(string, delim):
        return string.partition(delim)[2]


    with open(binary, 'rb') as f:
        elffile = ELFFile(f)

        for section in elffile.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue

            symbols = [sym.name for sym in section.iter_symbols() if sym]
            return [substr_after(name, PREPEND_SYM) for name in symbols
                    if name.startswith(PREPEND_SYM)]