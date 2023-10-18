def parse(self, native):
        """
        Parses a native configuration and converts
        it to a NetJSON configuration dictionary
        """
        if not hasattr(self, 'parser') or not self.parser:
            raise NotImplementedError('Parser class not specified')
        parser = self.parser(native)
        self.intermediate_data = parser.intermediate_data
        del parser
        self.to_netjson()