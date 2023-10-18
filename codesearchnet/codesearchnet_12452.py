def expand(self):
        """
        Returns all of its options as seperated sub-sentences.

        Returns:
            List<List<str>>: A list containing the sentences created by all
                                expansions of its sub-sentences
        """
        options = []
        for option in self._tree:
            options.extend(option.expand())
        return options