def prune(self, regex=r".*"):
        """
        Prune leaves of filetree according to specified
        regular expression.

        Args:
            regex (str): Regular expression to use in pruning tree.
        """
        return filetree(self.root, ignore=self.ignore, regex=regex)