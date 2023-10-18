def argparser(self):
        """
            Argparser option with search functionality specific for ranges.
        """
        core_parser = self.core_parser
        core_parser.add_argument('-r', '--range', type=str, help="The range to search for use")
        return core_parser