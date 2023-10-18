def name(self):
        """Concatenates the names of the given criteria in alphabetical order.

        If a sub-criterion is itself a combined criterion, its name is
        first split into the individual names and the names of the
        sub-sub criteria is used instead of the name of the sub-criterion.
        This is done recursively to ensure that the order and the hierarchy
        of the criteria does not influence the name.

        Returns
        -------
        str
            The alphabetically sorted names of the sub-criteria concatenated
            using double underscores between them.

        """
        names = (criterion.name() for criterion in self._criteria)
        return '__'.join(sorted(names))