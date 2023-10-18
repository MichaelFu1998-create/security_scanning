def get_associated_groups(self, element):
        """Returns a list of groups that an element (reaction, metabolite, gene)
        is associated with.

        Parameters
        ----------
        element: `cobra.Reaction`, `cobra.Metabolite`, or `cobra.Gene`

        Returns
        -------
        list of `cobra.Group`
            All groups that the provided object is a member of
        """
        # check whether the element is associated with the model
        return [g for g in self.groups if element in g.members]