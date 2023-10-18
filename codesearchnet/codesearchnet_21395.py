def argument_search(self):
        """
            Uses the command line arguments to fill the search function and call it.
        """
        arguments, _ = self.argparser.parse_known_args()
        return self.search(**vars(arguments))