def parse(type: Type):
        """
        Register a parser for a attribute type.

        Parsers will be used to parse `str` type objects from either
        the commandline arguments or environment variables.

        Args:
            type: the type the decorated function will be responsible
                for parsing a environment variable to.
        """

        def decorator(parser):
            EnvVar.parsers[type] = parser
            return parser

        return decorator