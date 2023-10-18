def resolve(self, symbol):
        """
        A helper method used to resolve a symbol name into a memory address when
        injecting hooks for analysis.

        :param symbol: function name to be resolved
        :type symbol: string

        :param line: if more functions present, optional line number can be included
        :type line: int or None
        """

        with open(self.binary_path, 'rb') as f:

            elffile = ELFFile(f)

            # iterate over sections and identify symbol table section
            for section in elffile.iter_sections():
                if not isinstance(section, SymbolTableSection):
                    continue

                # get list of symbols by name
                symbols = section.get_symbol_by_name(symbol)
                if not symbols:
                    continue

                # return first indexed memory address for the symbol,
                return symbols[0].entry['st_value']

            raise ValueError(f"The {self.binary_path} ELFfile does not contain symbol {symbol}")