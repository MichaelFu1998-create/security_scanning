def argument_count(self):
        """
            Uses the command line arguments to fill the count function and call it.
        """
        arguments, _ = self.argparser.parse_known_args()
        return self.count(**vars(arguments))